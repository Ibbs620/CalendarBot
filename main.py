from keep_alive import keep_alive
import discord
import os
import random
from datetime import datetime, timedelta
import asyncio
from discord.ext import commands, tasks

client = discord.Client()
video = ["https://cdn.discordapp.com/attachments/652528279634444309/799701542738460712/When_it_Monday.mp4","https://cdn.discordapp.com/attachments/652528279634444309/799701547973083146/When_it_Tuesday.mp4","https://cdn.discordapp.com/attachments/652528279634444309/799701549617512470/when_it_wednesday.mp4","https://cdn.discordapp.com/attachments/652528279634444309/799701547750916146/When_it_Thursday.mp4","https://cdn.discordapp.com/attachments/652528279634444309/799701551845081108/When_it_Friday.mp4","https://cdn.discordapp.com/attachments/652528279634444309/799701544458387516/When_it_Saturday.mp4","https://cdn.discordapp.com/attachments/652528279634444309/799701546974838824/When_It_Sunday.mp4"]
greeting = ["Good morning", "Top of the morning", "How's it going"]
name = ["ladies and gentlemen", "everyone", "groupchat"]
today = ["Today is", "It's", "It's finally"]
dayofweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

bot = commands.Bot("!")

target_channel_id = 794361878637707304

def getdayofweek():
  return (datetime.now() - timedelta(hours = 5)).weekday()

@bot.command()
async def commands(ctx):
  await ctx.channel.send(
    '```!commands\nLists all the commands (Including the one you just typed)\n\n!day\nTells you what day it is today\n\n!list <list>\nLists all the phrases in the selected list (greeting, name, today)\n\n!add <list> <phrase>\nAdds a phrase to the selected list (greeting, name, today). Phrase must be surrounded by "quotations".\n\n!remove <list> <index>\nRemoves a phrase from the selected list at the specified index. (Tip: use !list <list> to get the index number of the phrase)```')
@bot.command()
async def day(ctx):
    s= random.choice(today) + " " + dayofweek[getdayofweek()] + '.\n'
    await ctx.channel.send(s + video[getdayofweek()])

@bot.command()
async def add(ctx, arg1, arg2):
  if arg1 == 'greeting':
    greeting.append(arg2)
  elif arg1 == 'name':
    name.append(arg2)
  elif arg1 == 'today':
    today.append(arg2)
  else:
    await ctx.channel.send("Incorrect argument!")
    return
  await ctx.channel.send("Phrase " + "\"" + arg2 + "\" added to " + arg1 + ".")

@bot.command()
async def list(ctx, arg):
  it = 1
  s = ""
  if arg == 'greeting':
    await ctx.channel.send("Here is a list of greetings:")
    for i in greeting:
      s += str(it) + ": "+ i + '\n'
      it+=1
  elif arg == 'name':
    await ctx.channel.send("Here is a list of names:")
    for i in name:
      s += str(it) + ": "+ i + '\n'
      it+=1
  elif arg == 'today':
    await ctx.channel.send("Here is a list of today phrases:")
    for i in today:
      s += str(it) + ": "+ i + '\n'
      it+=1
  else:
    await ctx.channel.send("Incorrect argument!")
    return
  await ctx.channel.send(s)

@bot.command()
async def remove(ctx, arg, arg2):
  if arg == 'greeting':
    if int(arg2) > len(greeting):
      await ctx.channel.send("Index out of range!")
    else:
      greeting.pop(int(arg2)-1)
  elif arg == 'name':
    if int(arg2) > len(name):
      await ctx.channel.send("Index out of range!")
    else:
      name.pop(int(arg2) -1)
  elif arg == 'today':
    if int(arg2) > len(today):
      await ctx.channel.send("Index out of range!")
    else:
      today.pop(int(arg2)-1)
  else:
    await ctx.channel.send("Incorrect argument!")
    return
  await ctx.channel.send("Element removed!")

@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = bot.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    s = random.choice(greeting) + " " + random.choice(name) + "! " + random.choice(today) + " " + dayofweek[getdayofweek()] + '.\n'
    await message_channel.send(s + video[getdayofweek()])

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
    t = datetime(2021, 2, 10, 12, 45) - datetime.now()
    print(t.total_seconds())
    await asyncio.sleep(round(t.total_seconds()))
  

called_once_a_day.start()
keep_alive()
bot.run(os.getenv('TOKEN'))
client.run(os.getenv('TOKEN'))
