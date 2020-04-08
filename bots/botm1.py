import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4002)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} browser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
print ('---')

# Create a new channel
new_channel_name = input("Enter a new channel name: ")
if new_channel_name == "skip":
    pass
else:
    print(client.chat_channels.create(name=new_channel_name, type=1))

# List User Channels
channels = json.loads(client.chat_channels.list().content)["channels"]
print("Channels:")
print(channels)
my_channel = input("Get channel: ")
for c in channels:
    if my_channel in c.values():
        print("Found channel " + my_channel, c["id"])
        cid = c["id"]

# Get the first channel
channel_id = channels[0]['id']
channel_name = json.loads(client.chat_channels.get(channel_id=channel_id).content)['name']
print("First Channel ID: ")
print(channel_id)
print("First Channel name: ")
print(channel_name)

# update a channel
old_channel_name = input("Enter the channel you want to update: ")
new_channel_name = input("Enter the new channel name: ")
for c in channels:
    if old_channel_name in c.values():
        cid = c["id"]
        print(client.chat_channels.update(channel_id=cid, name=new_channel_name).content)


channels = json.loads(client.chat_channels.list().content)["channels"]

# Delete a channel
channel_name = input("Enter the channel name to be deleted: ")
for c in channels:
    if channel_name in c.values():
        cid = c["id"]
        print(client.chat_channels.delete(channel_id=cid).content)

# List channel members
channel_name = input("Enter the channel name to list members: ")
for c in channels:
    if channel_name in c.values():
        cid = c["id"]
members = json.loads(client.chat_channels.list_members(channel_id=cid).content)['members']
print(members)

# Invite channel members
channel_name = input("Enter the channel name to add members: ")
another_one = True
email_data = []
i = 0
while another_one and i < 5:
    member_email = input("Enter the email address of a member: ('n' to stop adding)")
    if member_email == "n":
        another_one = False
    else:
        email_data.append({"email": member_email})
        i += 1
print(email_data)
for c in channels:
    if channel_name in c.values():
        cid = c["id"]
print(client.chat_channels.invite_members(channel_id=cid, members=email_data).content)

# Leave a channel
channel_name = input("Enter the channel you want to leave: ")
for c in channels:
    if channel_name in c.values():
        cid = c["id"]
        print(client.chat_channels.leave_channel(channel_id=cid).content)

# Join the left channel
join_or_not = input("Join the channel again? y/n: ")
if join_or_not == "y":
    print(client.chat_channels.join_channel(channel_id=cid).content)

# Remove a member

channel_name = input("Enter the channel to remove a member: ")
member_id = input("Member to be deleted: ")
for c in channels:
    if channel_name in c.values():
        cid = c["id"]
        print(client.chat_channels.remove_member(channel_id=cid, member_id=member_id).content)


# List User Channels
channels = json.loads(client.chat_channels.list().content)["channels"]
print("Channels:")
print(channels)
my_channel = input("Enter channel name to test chat_messages: ")
for c in channels:
    if my_channel in c.values():
        print("Found channel " + my_channel, c["id"])
        cid = c["id"]

# send a message to the channel
message = input("Enter message: ")
print(client.chat_messages.post(to_channel=cid, message=message).content)

# List the messages of the channel
messages = json.loads(client.chat_messages.list(user_id='me', to_channel=cid).content)["messages"]
print("Previous messages of the channel:")
print(messages)

# update a message in channel
message = input("Update the last message to: ")
print(client.chat_messages.put(message_id=messages[len(messages)-1]['id'], message=message, to_channel=cid).content)


# delete the last message to the channel
print(messages[len(messages)-1]['id'])
option = input("Delete last message? y/n")
if option == "y":
    print(client.chat_messages.delete(message_id=messages[len(messages)-1]['id'], to_channel=cid).content)
