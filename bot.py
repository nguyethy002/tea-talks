import discord
from gtts import gTTS
import asyncio

# Define the prefix
PREFIX = "!"

# Define the intents
intents = discord.Intents.default()
intents.messages = True  # Enable message events
intents.message_content = True

# Create a Discord client with intents
client = discord.Client(intents=intents)

# Store the voice client globally
voice_client = None

# Function to split text into chunks of max_length
def split_text(text, max_length=1000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# Event to run when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event to run when a message is received
@client.event
async def on_message(message):
    global voice_client
    try:
        # Ignore messages from the bot itself to prevent a loop
        if message.author == client.user:
            return

        # Check if the message starts with the prefix
        if message.content.startswith(PREFIX):
            # Extract the command from the message
            command = message.content[len(PREFIX):].split()[0]

            # Check if the command is to disconnect the bot
            if command == "disconnect":
                if voice_client and voice_client.is_connected():
                    await voice_client.disconnect()
                    voice_client = None
                    await message.channel.send("Bot disconnected from voice channel.")
                else:
                    await message.channel.send("Bot is not connected to a voice channel.")
                return

            # Print the content of the message to the console
            print(f'Message from {message.author}: {message.content}')

            # Check if the author is in a voice channel
            if message.author.voice is None or message.author.voice.channel is None:
                await message.channel.send("You need to be in a voice channel to use this command.")
                return

            # Split the message content into smaller chunks
            text_chunks = split_text(message.content)

            # Connect to the voice channel if not already connected
            if voice_client is None or not voice_client.is_connected():
                voice_channel = message.author.voice.channel
                voice_client = await voice_channel.connect()

            # Convert each chunk to speech and play the audio
            for chunk in text_chunks:
                tts = gTTS(text=chunk, lang='vi')
                tts.save('message.mp3')
                voice_client.play(discord.FFmpegPCMAudio('message.mp3'), after=lambda e: print('done', e))

                # Wait until the audio is finished playing
                while voice_client.is_playing():
                    await asyncio.sleep(1)


    except Exception as e:
        print(f"An error occurred: {e}")

# Run the bot with your token
client.run('')
