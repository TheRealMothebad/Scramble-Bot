#base imports
from asyncio import tasks
from os import error
from discord.ext import commands
import discord, aiohttp, random, time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from trans_langs import langs

from tok import DontStealMyToken

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

g_translate = webdriver.Chrome(options=options)
out_box = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]'
crazyness = 5
delay = 4

bot = commands.Bot(command_prefix="`")

async def url_maker(tl, text_to_trans):
    return "https://translate.google.com/?sl=auto&tl="+tl+"&text="+text_to_trans+"&op=translate"

async def randomTranslate(ctx, sentence):
    next_l = random.choice(list(langs.keys()))
    await ctx.send("Next: " + langs.get(next_l))
    g_translate.get(await url_maker(next_l, sentence))
    time.sleep(delay)
    return g_translate.find_element_by_xpath(out_box).text

@bot.command(name="scramble", aliases=['s', 'garble'])
async def scramble(ctx, *, message):
    for x in range(1, crazyness):
        if x == 1:
            input_text = message
        input_text = await randomTranslate(ctx, input_text)
        #print(result)
        await ctx.send(input_text)
        if x == crazyness - 1:
            g_translate.get(await url_maker("en", input_text))
            time.sleep(delay)
            await ctx.send("Result:\n" + g_translate.find_element_by_xpath(out_box).text)

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