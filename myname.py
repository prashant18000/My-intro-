from telethon import TelegramClient, events, functions, types
import asyncio
import os
import cohere  

# --- 1. APNI TELEGRAM DETAILS YAHAN DAALEIN ---
api_id = 31643839  
api_hash = 'cb3f5e555c0b4fd0aa77ea7015bfce85'

# --- 2. APNI COHERE API KEY YAHAN DAALEIN ---
COHERE_API_KEY = 'AChEHieoD0gNJNfnRnLniK9nOWEX4fiod15FARvI'

cohere_client = cohere.Client(COHERE_API_KEY)
client = TelegramClient('alpha_master', api_id, api_hash)

# --- GLOBAL VARIABLES ---
tag_running = False
spam_running = False
tags_running = False           
tagsall_state = {}             
afk_mode = False
raid_active_users = {}       
infinite_raid_users = {}     
notebook = [] 
original_data = {"name": "", "pfp_path": None}

print("🛡️ Alpha Master Script Loading (Cohere AI + ALL OLD COMMANDS)...")

@client.on(events.NewMessage(outgoing=True))
async def manager(event):
    global tag_running, spam_running, tags_running, tagsall_state, afk_mode, notebook, original_data, raid_active_users, infinite_raid_users
    
    text = event.text

    # --- AFK Logic ---
    if afk_mode and not text == ".afk":
        afk_mode = False
        await event.respond("✅ **I'm back! AFK mode turned off.**", delete_after=5)

    # 1. PING & AFK
    if text == ".ping":
        await event.edit(f"🚀 **Alpha Master Bot is Online!**\n✅ **AI Status:** Active")
    elif text == ".afk":
        afk_mode = True
        await event.edit("💤 **AFK Mode Activated.**")

    # 🤖 2. THE AI ASK COMMAND (.ask) - FIXED (NO MODEL NAME)
    elif text.startswith(".ask "):
        question = text.replace(".ask ", "").strip()
        if not question:
            return await event.edit("❌ **Format:** `.ask [question]`")
        
        await event.edit("⏳ *AI soch raha hai...*")
        try:
            # Model name hata diya gaya hai taaki 'model removed' wala error na aaye
            response = cohere_client.chat(message=question)
            await event.edit(f"🗣️ **Q:** {question}\n\n🤖 **A:**\n{response.text}")
        except Exception as e:
            await event.edit(f"❌ **API Error:**\n`{str(e)}`")

    # 👑 3. THE STYLISH DETAIL COMMAND (.detail)
    elif text == ".detail":
        detail_msg = """
        ╔════════════════════════════╗
        ╠ 👑 𝕺𝖜𝖓𝖊𝖗 : ✨ 𝕯𝖊𝖘𝖈𝖊𝖓𝖙 𝕭𝖔𝖞𝖞 ✨
        ╠ 🌐 𝖀𝖘𝖊𝖗𝖓𝖆𝖒𝖊 : **@descent_boyy**
        ╚════════════════════════════╝
        📜 𝕮𝖔𝖒𝖒𝖆𝖓𝖉𝖘 𝕸𝖊𝖓𝖚 :
        ➪ `.𝖆𝖘𝖐 [𝖖𝖚𝖊𝖘𝖙𝖎𝖔𝖓]` : 𝕬𝕴 𝖘𝖊 𝖐𝖚𝖈𝖍 𝖇𝖍𝖎 𝖕𝖔𝖔𝖈𝖍𝖔.
        ➪ `.𝖙𝖆𝖌 [𝖓𝖔] [𝖒𝖘𝖌]` : 𝕾𝖕𝖆𝖒 𝖙𝖆𝖌 𝖔𝖓 𝖆 𝖚𝖘𝖊𝖗.
        ➪ `.𝖗𝖆𝖎𝖉` : (𝕽𝖊𝖕𝖑𝖞) 𝕬𝖚𝖙𝖔-𝖗𝖊𝖕𝖑𝖞 𝖗𝖆𝖎𝖉.
        ➪ `.𝖈𝖑𝖔𝖓𝖊` : (𝕽𝖊𝖕𝖑𝖞) 𝕮𝖔𝖕𝖞 𝖕𝖗𝖔𝖋𝖎𝖑𝖊.
        """
        await event.edit(detail_msg)

    # 4. CLONE & ENDCLONE
    elif text.startswith(".clone"):
        reply = await event.get_reply_message()
        if not reply: return await event.edit("❌ Reply to a user!")
        await event.edit("⌛ **Cloning Identity...**")
        try:
            user = await client.get_entity(reply.sender_id)
            me = await client.get_me()
            original_data["name"] = me.first_name
            my_photos = await client.get_profile_photos("me")
            if my_photos: original_data["pfp_path"] = await client.download_media(my_photos[0])
            user_photos = await client.get_profile_photos(user)
            if user_photos:
                path = await client.download_media(user_photos[0])
                await client(functions.photos.UploadProfilePhotoRequest(file=await client.upload_file(path)))
                if os.path.exists(path): os.remove(path)
            await client(functions.account.UpdateProfileRequest(first_name=user.first_name))
            await event.edit(f"✅ **Cloned:** {user.first_name}")
        except Exception as e: await event.edit(f"⚠️ Error: {e}")

    elif text == ".endclone":
        if not original_data["name"]: return await event.edit("❌ No backup found!")
        try:
            await client(functions.account.UpdateProfileRequest(first_name=original_data["name"]))
            if original_data["pfp_path"] and os.path.exists(original_data["pfp_path"]):
                await client(functions.photos.UploadProfilePhotoRequest(file=await client.upload_file(original_data["pfp_path"])))
                os.remove(original_data["pfp_path"])
                original_data["pfp_path"] = None
            await event.edit("✅ **Profile Restored!**")
        except Exception as e: await event.edit(f"⚠️ Error: {e}")

    # 5. SINGLE TAG (.tag) & STOP
    elif text.startswith(".tag "):
        reply = await event.get_reply_message()
        if not reply: return await event.edit("❌ Reply to a message!")
        try:
            parts = event.text.split(" ", 2)
            count, msg = int(parts[1]), parts[2]
            spam_running = True
            await event.delete()
            for _ in range(count):
                if not spam_running: break
                await reply.reply(msg)
                await asyncio.sleep(1.5)
        except: pass

    elif text == ".stop":
        spam_running = False
        raid_active_users.clear()
        await event.edit("🛑 **Stopped.**")

    # 6. UNIQUE TAGS (.tags & .stoptags)
    elif text.startswith(".tags "):
        reply = await event.get_reply_message()
        if not reply: return await event.edit("❌ Reply to a starting message!")
        try:
            parts = event.text.split(" ", 2)
            count = int(parts[1])
            msg_text = parts[2]
            tags_running = True
            await event.delete()
            replied_users = set()
            async for m in client.iter_messages(event.chat_id, min_id=reply.id, reverse=True):
                if not tags_running or count <= 0: break
                if not m.out and m.sender_id and m.sender_id not in replied_users:
                    await m.reply(msg_text)
                    replied_users.add(m.sender_id)
                    count -= 1
                    await asyncio.sleep(1.5)
        except: pass

    elif text == ".stoptags":
        tags_running = False
        await event.edit("🛑 **Stopped Unique Tags.**")

    # 7. GROUP MENTION (.tagall, .stopall)
    elif text.startswith(".tagall"):
        tag_running = True
        msg = event.text.replace(".tagall", "").strip() or "📢"
        await event.delete()
        async for u in client.iter_participants(event.chat_id):
            if not tag_running: break
            if not u.bot and not u.deleted:
                try:
                    await client.send_message(event.chat_id, f"{msg} [\u2063](tg://user?id={u.id}){u.first_name}")
                    await asyncio.sleep(3.5)
                except: continue

    elif text == ".stopall":
        tag_running = False
        await event.edit("🛑 **Stopped Group Tags.**")

    # 8. RAID COMMANDS
    elif text.startswith(".addraid"):
        lines = event.text.replace(".addraid", "").strip().split(",")
        for l in lines: notebook.append(l.strip())
        await event.edit(f"✅ **Added!** Total: {len(notebook)}")

    elif text == ".showraid":
        if not notebook: return await event.edit("❌ Empty!")
        res = "**📓 Notebook:**\n" + "\n".join([f"{i+1}. {l}" for i, l in enumerate(notebook)])
        await event.edit(res[:4000])

    elif text.startswith(".raid"):
        reply = await event.get_reply_message()
        if not reply or not notebook: return await event.edit("❌ Reply to Target!")
        try:
            start_idx = int(event.text.split(" ")[1]) - 1
            raid_active_users[reply.sender_id] = start_idx
            await event.edit(f"⚔️ **Raid Active!**")
        except: pass

    # 9. PURGE COMMANDS
    elif text.startswith(".purge"):
        await event.delete()
        try:
            count = int(event.text.split(" ")[1])
            async for m in client.iter_messages(event.chat_id, from_user="me", limit=count):
                await m.delete()
        except: pass

# --- INCOMING HANDLER ---
@client.on(events.NewMessage(incoming=True))
async def on_incoming(event):
    global afk_mode, raid_active_users, notebook
    
    if afk_mode and event.is_private:
        await event.reply("💤 Away from keyboard right now.")

    if event.sender_id in raid_active_users:
        idx = raid_active_users[event.sender_id]
        if idx < len(notebook):
            await event.reply(notebook[idx])
            raid_active_users[event.sender_id] += 1
        else: 
            del raid_active_users[event.sender_id]

async def start_bot():
    await client.start()
    print("🛡️ Alpha Master Bot Live (Final Complete Version)!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(start_bot())

