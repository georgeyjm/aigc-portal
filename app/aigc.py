import openai
import replicate
import discord

# from config import DEFAULT_PERSONALITY, BOT_NAME_IN_PROMPT, PARTIAL_RESPONSE_INDICATOR, MAX_LENGTH


MAX_LENGTH = 400
PARTIAL_RESPONSE_INDICATOR = '……'


def openai_chat(history, model='gpt-4', stream=True):
    response = openai.ChatCompletion.create(
        model=model,
        messages=history,
        temperature=1,
        max_tokens=MAX_LENGTH,
        stream=stream,
    )
    # TODO: Error handling

    if stream:
        for block in response:
            block_data = block.choices[0]
            block_text = block_data['delta'].get('content', '')
            yield block_text
    else:
        response_data = response['choices'][0]
        response_text = response_data['message']['content']
        if response_data['finish_reason'] == 'length':
            response_text += PARTIAL_RESPONSE_INDICATOR
        return response_text # response['usage']['completion_tokens']


def openai_complete(history, personality=None):
    prompt = '下面是你和一个人之间的对话。'
    if personality is None:
        prompt += DEFAULT_PERSONALITY
    else:
        prompt += personality
    prompt += '\n\n'
    for message in history:
        prompt += message.format('gpt')
    prompt += f'{BOT_NAME_IN_PROMPT}: '

    response = openai.Completion.create(
        # model='text-davinci-003',
        model='gpt-4',
        prompt=prompt,
        temperature=1.2,
        max_tokens=MAX_LENGTH
    )
    # TODO: Error handling
    response_data = response['choices'][0]
    response_text = response_data['text'].strip()
    if response_data['finish_reason'] == 'length':
        response_text += PARTIAL_RESPONSE_INDICATOR
    return response_text, response['usage']['completion_tokens']


def replicate_stable_diffusion(prompt):
    output = sd_version.predict(
        prompt=prompt,
        image_dimensions='768x768',
        num_outputs=1,
        num_inference_steps=50, # 1-500
        guidance_scale=7.5, # 1-20
        scheduler='DPMSolverMultistep'
        # seed=,
    )
    return output[0]


def replicate_midjourney(prompt):
    output = mj_version.predict(
        prompt=prompt,
        width=768,
        height=768,
        prompt_strength=0.8,
        num_outputs=1,
        num_inference_steps=50, # 1-500
        guidance_scale=7.5, # 1-20
        scheduler='DPMSolverMultistep'
        # seed=,
    )
    return output[0]


def replicate_openjourney(prompt):
    output = oj_version.predict(
        prompt=f'mdjrny-v4 style {prompt}',
        width=768,
        height=1024,
        num_outputs=1,
        num_inference_steps=50, # 1-500
        guidance_scale=6, # 1-20
        # seed=,
    )
    return output[0]


# class DiscordClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         # don't respond to ourselves
#         if message.author == self.user:
#             return

#         if message.content == 'ping':
#             await message.channel.send('pong')

# intents = discord.Intents.default()
# intents.message_content = True
# client = MyClient(intents=intents)
# client.run('token')


# def discord_midjourney(prompt):
#     async def msg(ctx, userid:str, *, msg):
#         user = client.get_member(userid) # user = ctx.message.server.get_member(userid)
#         await client.send_message(user,msg)


sd_model = replicate.models.get('stability-ai/stable-diffusion')
sd_version = sd_model.versions.get('db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf')

mj_model = replicate.models.get('tstramer/midjourney-diffusion')
mj_version = mj_model.versions.get('436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b')

oj_model = replicate.models.get('prompthero/openjourney')
oj_version = oj_model.versions.get('9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb')
