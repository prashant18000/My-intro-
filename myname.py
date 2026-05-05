import os, asyncio, time, requests
from telethon import TelegramClient, events, functions, types

# Aapki API Details
api_id = 31643839
api_hash = 'cb3f5e555c0b4fd0aa77ea7015bfce85'

client = TelegramClient('alpha_master', api_id, api_hash)

# --- Control Variables ---
tag_target_running = False
tags_auto_running = False
tags_auto_text = ""
tags_replied_users = set()

raids_running = False  
afk_status = False
afk_reason = ""
raids_msgs = ["Abey...", "Dum hai?", "Alpha is here!", "Tera baap aaya!", "Nikal lawde!", "Alpha power! ☠️"]

# 1. PING COMMAND
@client.on(events.NewMessage(pattern=r'^\.ping$'))
async def ping(event):
    start = time.time()
    msg = await event.edit("🚀 **Alpha is Online!**")
    end = time.time()
    ms = round((end - start) * 1000, 2)
    await msg.edit(f"🚀 **Alpha is Online!**\n`Latency: {ms}ms`")

# 2. HELP MENU
@client.on(events.NewMessage(pattern=r'^\.help$'))
async def help_menu(event):
    menu = """╔════════════════════════════╗
╠ 👑 𝕺𝖜𝖓𝖊𝖗 : ✨ ☠️𝓜𝓻. 𝓯𝓾𝓽𝓾𝓻𝓲𝓼𝓽𝓲𝓬 ☠️ ✨
╠ 🌐 𝖀𝖘𝖊𝖗𝖓𝖆𝖒𝖊 : @descent_boyy
╚════════════════════════════╝
📜 𝕮𝖔𝖒𝖒𝖆𝖓𝖉𝖘 𝕸𝖊𝖓𝖚 :
➪ .𝖆𝖘𝖐 | .𝖉𝖊𝖙𝖆𝖎𝖑
➪ .𝖙𝖆𝖌 | .𝖙𝖆𝖌𝖘 | .𝖙𝖆𝖌𝖆𝖑𝖑
➪ .𝖗𝖆𝖎𝖉 | .𝖗𝖆𝖎𝖉𝖘 | .𝖘𝖍𝖔𝖜𝖗𝖆𝖎𝖉
➪ .𝖈𝖑𝖔𝖓𝖊 | .𝖊𝖓𝖉𝖈𝖑𝖔𝖓𝖊 
➪ .𝖕𝖚𝖗𝖌𝖊 | .𝖕𝖚𝖗𝖌𝖊𝖆𝖑𝖑
➪ .𝖘𝖙𝖔𝖕 | .𝖘𝖙𝖔𝖕𝖆𝖑𝖑 | .𝖘𝖙𝖔𝖕𝖗𝖆𝖎𝖉 | .𝖘𝖙𝖔𝖕𝖙𝖆𝖌𝖘"""
    await event.edit(menu)

# 3. DETAIL MENU (Updated)
@client.on(events.NewMessage(pattern=r'^\.detail$'))
async def detail_menu(event):
    details = """📜 **ALPHA BOT COMMANDS DETAIL** 📜

✅ `.tag [text]` : Target ko infinite text spam karega. Rokne ke liye `.stop`.
✅ `.tags [text]` : Smart Auto-reply. Har naye message karne wale ko 1 baar text bhejega.
✅ `.stoptags` : `.tag` aur `.tags` dono ko rokne ke liye.
✅ `.raid` : Dushman ko 1 baar heavy lines bhejega.
✅ `.raids` : Infinite loop mein lines bhejega.
✅ `.stopraids` : Chalte hue raid ko rokne ke liye.
✅ `.purgeall` : Tumhare bheje hue SAARE messages delete karega.
✅ `.afk` : VIP Busy mode on karega.
✅ `.clone` : Reply karke DP, Name, Bio chura lega.
✅ `.stop` / `.stopall` : Master Kill-Switch (Sab kuch ek sath band)."""
    await event.edit(details)

# 4. SINGLE TARGET TAG (.tag [text])
@client.on(events.NewMessage(pattern=r'^\.tag (.*)'))
async def single_target_tag(event):
    global tag_target_running
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ **Bhai, jisko target karna hai uske message par reply karke command do!**")
    
    text = event.pattern_match.group(1)
    tag_target_running = True
    target_user = await client.get_entity(reply.sender_id)
    
    await event.edit(f"🚀 **Target Locked! Spamming {target_user.first_name}...**")
    
    while tag_target_running:
        try:
            await client.send_message(event.chat_id, f"[{target_user.first_name}](tg://user?id={target_user.id}) {text}")
            await asyncio.sleep(2)
        except:
            await asyncio.sleep(5)

# 5. SMART AUTO-REPLY TAGS (.tags [text])
@client.on(events.NewMessage(pattern=r'^\.tags (.*)'))
async def smart_auto_tags(event):
    global tags_auto_running, tags_auto_text, tags_replied_users
    tags_auto_text = event.pattern_match.group(1)
    tags_auto_running = True
    tags_replied_users.clear() # Purani list saaf
    await event.edit(f"🚀 **Smart Auto-Reply ON!**\nAb jo bhi message karega usko reply jayega: `{tags_auto_text}`")

# Auto-reply listener
@client.on(events.NewMessage(incoming=True))
async def handle_smart_tags(event):
    global tags_auto_running, tags_auto_text, tags_replied_users
    if tags_auto_running:
        sender_id = event.sender_id
        # Check agar user ko pehle reply nahi kiya hai
        if sender_id not in tags_replied_users:
            tags_replied_users.add(sender_id)
            try:
                await event.reply(tags_auto_text)
            except:
                pass

# 6. STOP TAGS
@client.on(events.NewMessage(pattern=r'^\.stoptags$'))
async def stop_tags(event):
    global tag_target_running, tags_auto_running
    tag_target_running = False
    tags_auto_running = False
    await event.edit("🛑 **Tagging & Smart Replies Stopped.**")

# 7. SINGLE RAID (.raid)
@client.on(events.NewMessage(pattern=r'^\.raid$'))
async def single_raid(event):
    await event.edit("🔥 **𝕽𝖆𝖎𝖉 𝕾𝖙𝖆𝖗𝖙𝖊𝖉! (Single Mode)**")
    for msg in raids_msgs:
        try:
            await event.respond(msg)
            await asyncio.sleep(1.5)
        except:
            pass
    await event.respond("✅ **Single Raid Complete!**")

# 8. INFINITE RAID (.raids)
@client.on(events.NewMessage(pattern=r'^\.raids$'))
async def infinite_raids(event):
    global raids_running
    if raids_running:
        return await event.edit("⚠️ **Infinite Raid pehle se chal rahi hai!**")
    raids_running = True
    await event.edit("🔥 **𝕽𝖆𝖎𝖉 𝕾𝖙𝖆𝖗𝖙𝖊𝖉! (Infinite Mode)**")
    while raids_running:
        for msg in raids_msgs:
            if not raids_running: break
            try:
                await event.respond(msg)
                await asyncio.sleep(1.5)
            except:
                await asyncio.sleep(5)

# 9. SHOW RAID & STOP RAIDS
@client.on(events.NewMessage(pattern=r'^\.showraid$'))
async def show_raid_list(event):
    msg_list = "\n".join([f"• {m}" for m in raids_msgs])
    await event.edit(f"📜 **Current Raid Messages:**\n\n{msg_list}")

@client.on(events.NewMessage(pattern=r'^\.stopraids?$'))
async def stop_raid_cmd(event):
    global raids_running
    raids_running = False
    await event.edit("🛑 **𝕽𝖆𝖎𝖉 𝕾𝖙𝖔𝖕𝖕𝖊𝖉 Successfully.**")

# 10. MASTER STOP
@client.on(events.NewMessage(pattern=r'^\.stopall|\.stop$'))
async def stop_all(event):
    global raids_running, tag_target_running, tags_auto_running
    raids_running = False
    tag_target_running = False
    tags_auto_running = False
    await event.edit("📴 **All Systems (Raids, Tags, Auto-replies) Stopped.**")

# 11. ASK AI
@client.on(events.NewMessage(pattern=r'^\.ask (.*)'))
async def ask_ai(event):
    question = event.pattern_match.group(1)
    await event.edit("🧠 **Thinking...**")
    try:
        url = f"https://chatgpt.apinepdev.workers.dev/?question={question}"
        response = requests.get(url).json()
        answer = response.get("answer", "No response.")
        await event.edit(f"🤖 **AI Answer:**\n{answer}")
    except:
        await event.edit("❌ **AI Busy hai.**")

# 12. PURGE & PURGEALL
@client.on(events.NewMessage(pattern=r'^\.purge (.*)'))
async def purge_msgs(event):
    count = int(event.pattern_match.group(1))
    await event.edit(f"🗑️ **Purging {count} messages...**")
    msgs = []
    async for m in client.iter_messages(event.chat_id, limit=count+1):
        msgs.append(m)
    await client.delete_messages(event.chat_id, msgs)

@client.on(events.NewMessage(pattern=r'^\.purgeall$'))
async def purge_all_msgs(event):
    await event.edit("🗑️ **Scan kar raha hu... Saare purane messages delete ho jayenge!**")
    count = 0
    msgs = []
    async for m in client.iter_messages(event.chat_id, from_user='me'):
        msgs.append(m)
        count += 1
        # 100 messages ka jhund banakar delete karega taaki error na aaye
        if len(msgs) == 100:
            await client.delete_messages(event.chat_id, msgs)
            msgs = []
    if msgs:
        await client.delete_messages(event.chat_id, msgs)
    
    rep = await event.respond(f"✅ **Successfully deleted SAARE ({count}) messages!**")
    await asyncio.sleep(3)
    await rep.delete()

# 13. CLONE
@client.on(events.NewMessage(pattern=r'^\.clone$'))
async def clone_all(event):
    reply = await event.get_reply_message()
    if not reply: return await event.edit("Reply to someone!")
    await event.edit("👤 **Cloning EVERYTHING...**")
    user = await client.get_entity(reply.sender_id)
    full = await client(functions.users.GetFullUserRequest(user.id))
    await client(functions.account.UpdateProfileRequest(first_name=user.first_name or "", last_name=user.last_name or "", about=full.full_user.about or ""))
    photo = await client.download_profile_photo(user.id)
    if photo:
        await client(functions.photos.UploadProfilePhotoRequest(file=await client.upload_file(photo)))
        os.remove(photo)
    await event.edit("✅ **Cloned!**")

# 14. AFK 
@client.on(events.NewMessage(pattern=r'^\.afk(?: |$)(.*)'))
async def set_afk(event):
    global afk_status, afk_reason
    afk_status = True
    default_reason = "Away at the moment\nWill respond once I’m back."
    afk_reason = event.pattern_match.group(1) or default_reason
    await event.edit(f"💤 **AFK Mode ON**\n\n**Reason:**\n`{afk_reason}`")

@client.on(events.NewMessage(incoming=True))
async def afk_rep(event):
    if afk_status and (event.is_private or event.mentioned):
        await event.reply(f"🤖 **Auto Reply:**\nOwner is currently AFK.\n\n**Reason:**\n`{afk_reason}`")

@client.on(events.NewMessage(outgoing=True))
async def off_afk(event):
    global afk_status
    if afk_status and not event.text.startswith(".afk"):
        afk_status = False
        await event.respond("✅ **Back Online! AFK mode removed.**")

print("Alpha Bot is LIVE with Smart Tags & Purgeall!")
client.start()
client.run_until_disconnected()
