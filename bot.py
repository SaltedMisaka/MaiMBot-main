import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from nonebot.drivers import Driver
from nonebot.log import default_filter, default_format, logger


def main() -> None:
    logger.add('logs/bot_{time:YYYY-MM-DD}.log',
               level=0,
               rotation='00:00',
               format=default_format,
               filter=default_filter)
    nonebot.init()

    driver: Driver = nonebot.get_driver()
    driver.register_adapter(OneBotV11Adapter)

    nonebot.load_builtin_plugins('echo')
    # nonebot.load_plugin('src.plugins.help')
    # nonebot.load_plugin('src.plugins.blacklist')
    # nonebot.load_plugin('src.plugins.fwdrequests')
    # nonebot.load_plugin('src.plugins.runcode')
    # nonebot.load_plugin('src.plugins.sklassistant')
    # nonebot.load_plugin('src.plugins.chat')
    # nonebot.load_plugin('src.plugins.maimai')
    # nonebot.load_plugin('src.plugins.autoreply')
    # nonebot.load_plugin('src.plugins.slscq')
    # nonebot.load_plugin('src.plugins.biliinfo')
    # nonebot.load_plugin('src.plugins.roll')
    # nonebot.load_plugin('src.plugins.poke')
    # nonebot.load_plugin('src.plugins.simplemusic')
    # nonebot.load_plugin('src.plugins.repeater')
    # nonebot.load_plugin('src.plugins.boardgame')
    # nonebot.load_plugin('src.plugins.text2sound')
    # nonebot.load_plugin('src.plugins.xxivgame')
    # nonebot.load_plugin('src.plugins.homo')
    # nonebot.load_plugin('src.plugins.mahjong')
    # nonebot.load_plugin('src.plugins.answersbook')
    # nonebot.load_plugin('src.plugins.tygj')
    # nonebot.load_plugin('src.plugins.revoke')
    # nonebot.load_plugin('src.plugins.ncm')
    # nonebot.load_plugin('src.plugins.abbreply')
    # nonebot.load_plugin('src.plugins.kfccrazythu')
    # nonebot.load_plugin('src.plugins.choose')
    # nonebot.load_plugin('src.plugins.wordle')
    # nonebot.load_plugin('src.plugins.handle')

    # nonebot.load_plugin('nonebot_plugin_emojimix')
    # nonebot.load_plugin('nonebot_plugin_abstract')
    # nonebot.load_plugin('nonebot_plugin_makemidi')
    # nonebot.load_plugin('nonebot_plugin_wordcloud')
    # nonebot.load_plugin('nonebot_plugin_memes')

    nonebot.run()


if __name__ == '__main__':
    main()