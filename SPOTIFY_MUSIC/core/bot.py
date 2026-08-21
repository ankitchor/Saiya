# ======================================================================
# ||                                                               ||
# ||   ██████╗  █████╗ ██████╗ ██╗   ██╗███████╗███████╗██╗ ██████╗  ||
# ||   ██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██║██╔═══██╗ ||
# ||   ██████╔╝███████║██████╔╝██║   ██║█████╗  ███████╗██║██║   ██║ ||
# ||   ██╔══██╗██╔══██║██╔══██╗██║   ██║██╔══╝  ╚════██║██║██║▄▄ ██║ ||
# ||   ██████╔╝██║  ██║██████╔╝╚██████╔╝███████╗███████║██║╚██████╔╝ ||
# ||   ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚══════╝╚══════╝╚══════╝╚═╝ ╚══▀▀═╝  ||
# ||                                                               ||
# ======================================================================

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class BABY(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")

        super().__init__(
            name="SPOTIFY_MUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        # ---------------------------------------------------------
        # START BOT
        # ---------------------------------------------------------
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        LOGGER(__name__).info(
            f"Bot started: @{self.username} | ID: {self.id}"
        )

        # ---------------------------------------------------------
        # CHECK LOGGER ID
        # ---------------------------------------------------------
        try:
            logger_id = int(config.LOGGER_ID)
        except (ValueError, TypeError):
            LOGGER(__name__).error(
                "LOGGER_ID is invalid. It must be a numeric Telegram chat ID."
            )
            LOGGER(__name__).warning(
                "Example: -1001234567890"
            )

            # Logger invalid hai, lekin bot ko crash mat karo.
            LOGGER(__name__).warning(
                "Bot will continue without log-group access."
            )
            return

        # ---------------------------------------------------------
        # SEND START MESSAGE TO LOG GROUP / CHANNEL
        # ---------------------------------------------------------
        try:
            await self.send_message(
                chat_id=logger_id,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )

            LOGGER(__name__).info(
                f"Successfully connected to LOGGER_ID: {logger_id}"
            )

        # ---------------------------------------------------------
        # TELEGRAM LOGGER ERRORS
        # ---------------------------------------------------------
        except errors.PeerIdInvalid:
            LOGGER(__name__).error(
                f"LOGGER_ID is invalid or bot cannot find chat: {logger_id}"
            )
            LOGGER(__name__).warning(
                "Check that the bot has been added to the log group/channel."
            )

        except errors.ChannelInvalid:
            LOGGER(__name__).error(
                f"Telegram rejected LOGGER_ID: {logger_id}"
            )
            LOGGER(__name__).warning(
                "Check the log channel/group ID."
            )

        except errors.ChatIdInvalid:
            LOGGER(__name__).error(
                f"Invalid Telegram chat ID: {logger_id}"
            )

        except errors.ChatWriteForbidden:
            LOGGER(__name__).error(
                "Bot cannot send messages to the LOGGER_ID chat."
            )
            LOGGER(__name__).warning(
                "Add the bot to the group/channel and give required permissions."
            )

        except errors.UserNotParticipant:
            LOGGER(__name__).error(
                "Bot is not a member of the LOGGER_ID chat."
            )

        except errors.ChannelPrivate:
            LOGGER(__name__).error(
                "LOGGER_ID points to a private channel/group that the bot cannot access."
            )

        except Exception as ex:
            # IMPORTANT:
            # Pehle sirf ValueError print hota tha.
            # Ab complete error log hoga.
            LOGGER(__name__).exception(
                f"LOGGER GROUP ERROR: {type(ex).__name__}: {ex}"
            )

        # ---------------------------------------------------------
        # CHECK BOT ADMIN STATUS
        # ---------------------------------------------------------
        try:
            member = await self.get_chat_member(
                chat_id=logger_id,
                user_id=self.id,
            )

            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).warning(
                    "Bot is not an administrator in the LOGGER_ID chat."
                )
                LOGGER(__name__).warning(
                    "Please promote the bot as administrator."
                )
            else:
                LOGGER(__name__).info(
                    "Bot is administrator in the log group/channel."
                )

        except errors.UserNotParticipant:
            LOGGER(__name__).warning(
                "Bot is not a member of the LOGGER_ID chat."
            )

        except errors.PeerIdInvalid:
            LOGGER(__name__).warning(
                "Telegram could not resolve LOGGER_ID."
            )

        except errors.ChatAdminRequired:
            LOGGER(__name__).warning(
                "Admin permission is required to check the bot's status."
            )

        except errors.ChannelPrivate:
            LOGGER(__name__).warning(
                "LOGGER_ID chat is private or inaccessible."
            )

        except Exception as ex:
            LOGGER(__name__).exception(
                f"LOGGER MEMBER CHECK ERROR: {type(ex).__name__}: {ex}"
            )

        # ---------------------------------------------------------
        # BOT COMPLETELY STARTED
        # ---------------------------------------------------------
        LOGGER(__name__).info(
            f"Music Bot Started Successfully as {self.name}"
        )

    async def stop(self):
        LOGGER(__name__).info("Stopping Music Bot...")
        await super().stop()
