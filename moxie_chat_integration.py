import tiktoken
import moxie_circuits

class MoxieChat:
    def __init__(self):
        self.enc = tiktoken.encoding_for_model("gpt-4")
        self.messages = []

    def get_num_tokens(self, text):
        return len(self.enc.encode(text))

    def add_message(self, user, content):
        new_message = f"{user}: {content}"
        new_tokens = self.get_num_tokens(new_message)

        # If adding new message would exceed 2048 tokens, 
        # remove messages from the start until it would fit.
        while len(self.messages) > 0 and new_tokens + self.total_tokens() > 2048:
            removed_message = self.messages.pop(0)
            removed_tokens = self.get_num_tokens(removed_message)
            new_tokens -= removed_tokens

        self.messages.append(new_message)

    def total_tokens(self):
        return sum(self.get_num_tokens(msg) for msg in self.messages)

    def get_chat_history(self):
        if not self.messages:
            return "HISTORY:\n\nCURRENT_MESSAGE:"

        history = "\n".join(self.messages[:-1])
        current_message = self.messages[-1]
        return f"HISTORY:\n{history}\n\nCURRENT_MESSAGE: {current_message}"
    
    async def receive_message(self, user, content): 
        self.add_message(user, content)
        chat_history = self.get_chat_history()
        
        if await moxie_circuits.discriminate_chat_message(chat_history):
            dice_rolls = await moxie_circuits.extract_dice_rolls(chat_history)

            if dice_rolls != None:
                chat_history += "\n\n" + """
                DICE_RESULTS: {}
                """.format(dice_rolls)

            reply = await moxie_circuits.reply_to_chat_message(chat_history)
            self.add_message(user, reply)
            return reply