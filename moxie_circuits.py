import moxie_prompts
import moxie_core
import moxie_dice
import asyncio

async def discriminate_chat_message(chat_log):
    reply = await asyncio.to_thread(lambda: moxie_core.send_prompt_to_gpt(moxie_prompts.chat_discriminator_prompt, chat_log))

    if reply == "YES":
        return True
    else:
        return False

async def extract_dice_rolls(chat_log):
    reply = await asyncio.to_thread(lambda: moxie_core.send_prompt_to_gpt(moxie_prompts.dice_roller_prompt, chat_log))
    return await asyncio.to_thread(lambda: moxie_dice.roll_dice_from_json(reply))
    
async def reply_to_chat_message(chat_log):
    return await asyncio.to_thread(lambda: moxie_core.send_prompt_to_gpt(moxie_prompts.personality_prompt, chat_log, creative=True))