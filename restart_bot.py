from telethon import TelegramClient, events
import paramiko
import config
import os

# Replace these with your own Telegram bot details
api_id = config.API_ID  # Get from https://my.telegram.org/auth
api_hash = config.API_HASH  # Get from https://my.telegram.org/auth
bot_token = "7835088329:AAEBvgV8VmAMRBEnQ8qEVAypdgRqnTI8aHU"  # Get from BotFather
admins = [1061254944, 5415792594]
# VPS credentials
vps_ip = '195.248.243.253'
vps_username = 'root'
vps_password = 'k%h0He:Hf%@o=QLe1Xx!e]s~=j8kn>Y}Cp#Gin1:Z%q]}>#_h}tz:QHgyzT!azm,hg1wexXP9nor6w!i631asAA.dyPQVL^mW)3h'

# The name of the service to restart
service_name = 'f1_bot'

# Create the Telethon client
print("connecting...")
os.remove("restart_bot.session")
client = TelegramClient('restart_bot', api_id, api_hash).start(bot_token=bot_token)
print("connected!")
# Event handler for the '/restart' command
@client.on(events.NewMessage(pattern='/restart'))
async def restart_bot(event):
    user = event.sender_id

    # Send a "processing" message to the user
    await event.reply('Connecting to the server and restarting the bot...')

    try:
        # Establish SSH connection to VPS
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps_ip, username=vps_username, password=vps_password)

        # Run the restart command
        stdin, stdout, stderr = ssh.exec_command(f'sudo systemctl restart {service_name}')

        # Wait for the command to finish
        stdout.channel.recv_exit_status()

        # Check for errors in stderr
        error_message = stderr.read().decode('utf-8')
        if error_message:
            raise Exception(f"Error: {error_message}")

        # Close the SSH connection
        ssh.close()

        # Send success message to the user
        await event.reply('Bot has been successfully restarted on the server.')

    except Exception as e:
        # Handle any errors
        await event.reply(f'Failed to restart the bot. Error: {str(e)}')
@client.on(events.NewMessage(pattern='/stop'))
async def restart_bot(event):
    user = event.sender_id

    # Send a "processing" message to the user
    await event.reply('Connecting to the server and restarting the bot...')

    try:
        # Establish SSH connection to VPS
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps_ip, username=vps_username, password=vps_password)

        # Run the restart command
        stdin, stdout, stderr = ssh.exec_command(f'sudo systemctl restart {service_name}')

        # Wait for the command to finish
        stdout.channel.recv_exit_status()

        # Check for errors in stderr
        error_message = stderr.read().decode('utf-8')
        if error_message:
            raise Exception(f"Error: {error_message}")

        # Close the SSH connection
        ssh.close()

        # Send success message to the user
        await event.reply('Bot has been successfully stoped on the server.')

    except Exception as e:
        # Handle any errors
        await event.reply(f'Failed to stop the bot. Error: {str(e)}')

# Start the bot
client.run_until_disconnected()
