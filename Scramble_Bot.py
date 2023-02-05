#base imports
from asyncio import tasks
from os import error
from discord.ext import commands
import discord, aiohttp, random, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from trans_langs import langs

#import token from seperate file to avoid token leaking
from tok import DontStealMyToken

#start a webdriver (webscraper) with fun and spicy options
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
g_translate = webdriver.Chrome(options=options)

#the xpath to the google translate text output
out_box = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]'

#variables to control bot behavior
crazyness = 8
delay = 4

bot = commands.Bot(command_prefix="`")

#generate a url with the text to translate embeded
async def url_maker(tl, text_to_trans):
    return "https://translate.google.com/?sl=auto&tl="+tl+"&text="+text_to_trans+"&op=translate"

#translate the given sentence to a random lanuage
async def randomTranslate(ctx, sentence):
    next_l = random.choice(list(langs.keys()))
    await ctx.send("Next: " + langs.get(next_l))
    g_translate.get(await url_maker(next_l, sentence))
    time.sleep(delay)
    return g_translate.find_element_by_xpath(out_box).text

#scramble the given message "crazy" amount of times
#(I promise I have gotten better at naming variables since this was written)
@bot.command(name="scramble", aliases=['s', 'garble'])
async def scramble(ctx, *, message):
    "scrambles whatever sentence you put after the command"
    for x in range(1, crazyness):
        if x == 1:
            input_text = message
        input_text = await randomTranslate(ctx, input_text)
        await ctx.send(input_text)
        if x == crazyness - 1:
            g_translate.get(await url_maker("en", input_text))
            time.sleep(delay)
            await ctx.send("Result:\n" + g_translate.find_element_by_xpath(out_box).text)

@bot.command(name="delay")
@commands.is_owner()
async def setDelay(ctx, msg):
    global delay
    try:
        if int(msg) >= 4 and int(msg) <= 10:
            delay = int(msg)
            await ctx.send("Delay has been changed to: " + str(delay))
    except:
        await ctx.send("You did an oopsie :')  (must be a number between 4 and 10 inclusive")

@bot.command(name="crazy", aliases=["c", "iterations", "loops", "translations"])
async def setCrazy(ctx, msg):
    global crazyness
    try:
        if int(msg) >= 2 and int(msg) <= 12:
            crazyness = int(msg)
            await ctx.send("Crazyness has been changed to: " + str(crazyness))
    except:
        await ctx.send("You did an oopsie :')  (must be a number between 2 and 12 inclusive")




@bot.command(name="stop")
@commands.is_owner()
async def shutdown(ctx):
    "shuts down bot of command issuer is the same as dev acc for bot"
    await ctx.send("seeya")
    await ctx.bot.close()

@bot.event
async def on_command_error(ctx, error):
    #my approach to this is just have an if else chain to catch errors...
    if isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.send("You are not cool enough to do that.")

bot.run(DontStealMyToken)

g_translate.quit()
