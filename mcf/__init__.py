import asyncio
import nextcord
import GoldyBot

from . import _forms_, _info_, _tournament_, _player_

from GoldyBot.utility.datetime.user_input import *
from GoldyBot.utility.commands import *

class MCF(GoldyBot.Extenstion):
    def __init__(self, package_module=None):
        super().__init__(self, package_module_name=package_module)

        self.tournament:_tournament_.MCFTournament = None

        # Embeds
        #==========
        self.no_mcf_embed = GoldyBot.utility.goldy.embed.Embed(
            title="⛔ SignUps not open yet!",
            description=f"""
            ❌ *Sorry we haven't open signups for the next mcf yet.*
            """,
            colour=GoldyBot.utility.goldy.colours.AKI_RED
        )

        self.youve_been_removed_embed = GoldyBot.utility.goldy.embed.Embed(
            title="🧳 You've been removed!",
            description=f"""
            🚚 You've been removed from this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.WHITE
        )

        self.your_not_in_this_weeks_mcf_embed = GoldyBot.utility.goldy.embed.Embed(
            title="❤ Your not in this weeks mcf!",
            description=f"""
            ⚠ Your not registered for this week's mcf.
            """,
            colour=GoldyBot.utility.goldy.colours.RED
        )

    def loader(self):
        @GoldyBot.command(slash_cmd_only=True)
        async def mcf(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            self.tournament = await _info_.TournamentInfo().get_latest_mcf()

            if not self.tournament == None:
                return True # Your good to continue to the sub command.

            else:
                # No mcf available.
                message = await send(ctx, embed=self.no_mcf_embed)

                await asyncio.sleep(6)

                await message.delete()

                # Stop right here! Don't continue!
                return False



        @mcf.sub_command(help_des="An amazing command to sign up for the mcf minecraft tournament right from the confort of Discord.")
        async def join(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            # Check if a joinable mcf tournament exists.

            await ctx.send_modal(_forms_.JoinMCFForm(self.tournament))


        
        @mcf.sub_command(help_des="A command for players to leave this week's mcf tournament.")
        async def leave(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            # Check if a joinable mcf tournament exists.
            member = GoldyBot.Member(ctx)
            
            # Check if player is registered.
            if await self.tournament.is_member_registered(member):
                # If registered remove the player.
                await self.tournament.remove_player(await self.tournament.get_player(member))
                await send(ctx, embed=self.youve_been_removed_embed)

        @mcf.sub_command(help_des="Admin command to open the mcf minecraft tournament forum.", required_roles=["nova_staff"], also_run_parent_CMD=False)
        async def open_form(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            await ctx.send_modal(_forms_.OpenMCFForm())

        @mcf.sub_command(help_des="Admin command for canceling an MCF tournament.", required_roles=["nova_staff"], also_run_parent_CMD=False)
        async def cancel(self:MCF, ctx:GoldyBot.objects.slash.InteractionToCtx):
            tournament_info = _info_.TournamentInfo()
            
            view = _forms_.MCFCancelDropdownView(GoldyBot.Member(ctx), await tournament_info.get_all_mcfs())

            await send(ctx, embed=GoldyBot.utility.goldy.embed.Embed(
                title="🛑 Which MCF?",
                description="**⏱ Pick the mcf you would like to cancel.**",
                colour=GoldyBot.utility.goldy.colours.WHITE
            ), view=view)