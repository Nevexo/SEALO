import discord
from discord.ext import commands
import asyncio, json, os, datetime, logging, re, requests
from cogs.dict import define
from cogs.isup import isup

makesURL = ['bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co', 'tinylink.cf']
with open('config.json') as json_data_file:
    config = json.load(json_data_file)
def admin(message):
    if message.author.id in config['admins']['admins']:
        return True
    else:
        return False

if os.path.isdir("logs") == False: #Setting up logging:
    os.makedirs("logs/")
logfile = "logs/" + datetime.datetime.now().strftime('discordlog_%Y-%m-%d_%H-%M.log')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
print("Session log file: ", logfile)

print("Cold starting.")
print("(              (       )   ")
print(" )\ )     (     )\ ) ( /(   ")
print("(()/((    )\   (()/( )\())  ")
print(" /(_))\((((_)(  /(_)|(_)\   ")
print("(_))((_))\ _ )\(_))   ((_)  ")
print("/ __| __(_)_\(_) |   / _ \  ")
print("\__ \ _| / _ \ | |__| (_) | ")
print("|___/___/_/ \_\|____|\___/")
print("Version: " + str(config['info']['version']) + "| " +str(config['info']['motd']))

class cmds:
    def __init__(self, bot):
        self.bot=bot

    @commands.command(pass_content=True)
    async def urban(self, ctx, *, arg: str):
        embed = discord.Embed()
        embed.title = "Urban Dic | " + str(arg)
        embed.description = "Getting content... Twiddle your thumbs for a minute."
        embed.color = discord.Color.dark_gold()
        msg = await ctx.send(embed=embed)
        defi = define.urban(str(arg))
        if defi == False:
            embed.description = "noffin' found! bet u didn't even type some real ting did u, don't fuk with me!"
            embed.color = discord.Color.red()
        else:
            embed.color = discord.Color.blue()
            embed.description = defi
        await msg.edit(embed=embed)

    @commands.command(pass_content=True)
    async def info(self, ctx):
        #count = str(len(client.servers)) #Gotta find out how to do that in discord.ext
        Embed = discord.Embed()
        Embed.color = discord.Color.green()
        Embed.title = "SEALO FONOINFO."
        Embed.description = "Here's some awesome-sauce info about me."
        Embed.set_footer(text="Flap")
        Embed.add_field(name="Uptime", value="I've been flapping now for {0}".format("I forgot to add uptime."), inline=True)
        Embed.add_field(name="Servers", value="I'm in {0} servers. I live here, not there.".format("I need to work out how to do this in discord.ext"), inline=True)
        Embed.add_field(name="Version n' stuff", value="I'm rocking SEALO {0} ({0}.{1})".format(str(config['info']['version']), str(config['info']['build'])), inline=True)
        await ctx.send(embed=Embed)

    @commands.command(pass_content=True)
    async def wiki(self, ctx, *, arg: str):
        embed = discord.Embed()
        embed.title = "Wikipedia | " + str(arg)
        embed.description = "Just chill there u lil' one, getting content from Wikipedia!"
        embed.color = discord.Color.dark_gold()
        msg = await ctx.send(embed=embed)
        defi = define.wiki(str(arg))
        if defi == False:
            embed.description = "Sorry, that artcle wasn't found..."
            embed.color = discord.Color.red()
        else:
            embed.description = str(defi)
            embed.color = discord.Color.blue()
        await msg.edit(embed=embed)

    async def on_message(self, message):
        if message.author == self.bot.user: return
        OPERATE = False
        for i in makesURL:
            if OPERATE == False:
                if i in message.content:
                    Embed = discord.Embed()
                    OPERATE = True
                    Embed.set_author(name="", url="")
                    Embed.set_thumbnail(url="")
                    Embed.color = discord.Color.red()
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
                    runTimes = 1
                    Embed.title = "Spoopy URL Checker"
                    Embed.description = "Found " + str(len(urls)) + " short URL(s), I'll follow them and see where they go."
                    msg = await message.channel.send(embed=Embed)
                    followedURLS = []
                    for i in urls:
                        inputURL = i
                        try:
                            url = requests.head(inputURL).headers['location']
                            followedURLS.append(url)
                        except:
                            followedURLS.append("Failed to follow this URL, sorry.")
                        runTimes = runTimes + 1
                    string = ""
                    runTimes = 1
                    if len(followedURLS) == 0:
                        await client.delete_message(msg)
                    else:
                        for i in followedURLS:
                            string = string + "\n URL " + str(runTimes) + ": " + i
                            runTimes = runTimes + 1
                        Embed.description = string
                        Embed.set_footer(text="Remember, these links are spoopy and can get your IP address. Be careful my son.")
                        await msg.edit(embed=Embed)



bot = commands.Bot(command_prefix=commands.when_mentioned_or('~'), description='SEALO Helpie')
bot.add_cog(cmds(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))


bot.run(config['tokens']['token'])
