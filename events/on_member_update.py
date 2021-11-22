import discord


async def onMemberUpdate(oldState, newState, client):
    if(newState.id != client.user.id):
        return
    if(oldState.desktop_status == newState.desktop_status and oldState.mobile_status == newState.mobile_status):
        return
    if(str(newState.desktop_status) != "offline" or str(newState.mobile_status) != "offline"):
        if(str(oldState.desktop_status) == "offline" and str(oldState.mobile_status) == "offline"):
            await client.change_presence(activity=discord.CustomActivity(""), status=discord.Status.do_not_disturb, afk=False)
        
        return

    activity = discord.CustomActivity("currently unavalible", emoji="❌")
    await client.change_presence(status=discord.Status.idle, activity=activity, afk=True)