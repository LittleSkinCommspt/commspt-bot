from csllogparser import cslHandler
s = '''[2020-05-20 17:56:49] [Client thread INFO] CustomSkinLoader 14.12-SNAPSHOT-105
[2020-05-20 17:56:49] [Client thread INFO] DataDir: D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader
[2020-05-20 17:56:49] [Client thread INFO] Minecraft: 1.14.4(1.14.4)
[2020-05-20 17:56:49] [Client thread INFO] Config File: D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\CustomSkinLoader.json
[2020-05-20 17:56:49] [Client thread INFO] Try to load config.
[2020-05-20 17:56:49] [Client thread INFO] Successfully load config.
[2020-05-20 17:56:49] [Client thread INFO] version : 14.12
[2020-05-20 17:56:49] [Client thread INFO] enableDynamicSkull : true
[2020-05-20 17:56:49] [Client thread INFO] enableTransparentSkin : true
[2020-05-20 17:56:49] [Client thread INFO] ignoreHttpsCertificate : false
[2020-05-20 17:56:49] [Client thread INFO] forceLoadAllTextures : false
[2020-05-20 17:56:49] [Client thread INFO] enableCape : true
[2020-05-20 17:56:49] [Client thread INFO] cacheExpiry : 30
[2020-05-20 17:56:49] [Client thread INFO] enableUpdateSkull : false
[2020-05-20 17:56:49] [Client thread INFO] enableLocalProfileCache : false
[2020-05-20 17:56:49] [Client thread INFO] enableCacheAutoClean : false
[2020-05-20 17:56:49] [Client thread INFO] loadList : 7
[2020-05-20 17:57:13] [IceNoMC's skull INFO] Loading IceNoMC's profile.
[2020-05-20 17:57:13] [IceNoMC INFO] Loading IceNoMC's profile.
[2020-05-20 17:57:13] [IceNoMC INFO] 1/7 Try to load profile from 'Mojang'.
[2020-05-20 17:57:13] [IceNoMC's skull INFO] 1/7 Try to load profile from 'Mojang'.
[2020-05-20 17:57:13] [IceNoMC's skull DEBUG] Try to request 'https://api.mojang.com/profiles/minecraft'.
[2020-05-20 17:57:13] [IceNoMC's skull INFO] Payload: ["IceNoMC"]
[2020-05-20 17:57:13] [IceNoMC DEBUG] Try to request 'https://api.mojang.com/profiles/minecraft'.
[2020-05-20 17:57:13] [IceNoMC INFO] Payload: ["IceNoMC"]
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Successfully request (Response Code: 200 , Content Length: 2)
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Content: []
[2020-05-20 17:57:15] [IceNoMC's skull INFO] Profile not found.(IceNoMC's profile not found.)
[2020-05-20 17:57:15] [IceNoMC's skull INFO] 2/7 Try to load profile from 'LittleSkin'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Try to request 'https://littleskin.cn/IceNoMC.json'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Cache file found (Length: 3 , Path: 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\d117f8465e833ba5c4bd5152568719f4110d9622' , Expire: 1589982044')
[2020-05-20 17:57:15] [IceNoMC's skull INFO] Try to load from cache 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\d117f8465e833ba5c4bd5152568719f4110d9622'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Successfully load from cache
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Content: {}

[2020-05-20 17:57:15] [IceNoMC's skull INFO] Both skin and cape not found.
[2020-05-20 17:57:15] [IceNoMC's skull INFO] 3/7 Try to load profile from 'BlessingSkin'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Try to request 'http://skin.prinzeugen.net/IceNoMC.json'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Failed to request (Response Code: 404)
[2020-05-20 17:57:15] [IceNoMC's skull INFO] Profile not found.
[2020-05-20 17:57:15] [IceNoMC's skull INFO] 4/7 Try to load profile from 'ElyBy'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Try to request 'http://skinsystem.ely.by/textures/IceNoMC?version=2&minecraft_version=1.14.4'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Cache file found (Length: 0 , Path: 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\a2242fe09de4ac57cd65dcd1b86247f7487d735f' , Expire: 1589971244')
[2020-05-20 17:57:15] [IceNoMC's skull INFO] Try to load from cache 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\a2242fe09de4ac57cd65dcd1b86247f7487d735f'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Successfully load from cache
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Content: 
[2020-05-20 17:57:15] [IceNoMC's skull INFO] Profile not found.
[2020-05-20 17:57:15] [IceNoMC's skull INFO] 5/7 Try to load profile from 'SkinMe'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Try to request 'http://www.skinme.cc/uniskin/IceNoMC.json'.
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Successfully request (Response Code: 200 , Content Length: 37)
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Saved to cache (Length: 37 , Path: 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\0d488552b3ffef4da5e56fa2b43ed5bcb6927675' , Expire: 1589968727)
[2020-05-20 17:57:15] [IceNoMC's skull DEBUG] Content: {"errno":404,"msg":"User not found."}
[2020-05-20 17:57:15] [IceNoMC's skull INFO] Error 404: User not found.
[2020-05-20 17:57:15] [IceNoMC's skull INFO] 6/7 Try to load profile from 'LocalSkin'.
[2020-05-20 17:57:15] [IceNoMC's skull INFO] IceNoMC's profile loaded.
[2020-05-20 17:57:15] [IceNoMC's skull INFO] (SkinUrl: (LOCAL_LEGACY)d36e8c6d85f2cbc30993294b9314ecfa6809607b,LocalSkin/skins/IceNoMC.png , Model: auto , CapeUrl: null  , Expiry: 1589968667)
[2020-05-20 17:57:17] [IceNoMC DEBUG] Successfully request (Response Code: 200 , Content Length: 2)
[2020-05-20 17:57:17] [IceNoMC DEBUG] Content: []
[2020-05-20 17:57:17] [IceNoMC INFO] Profile not found.(IceNoMC's profile not found.)
[2020-05-20 17:57:17] [IceNoMC INFO] 2/7 Try to load profile from 'LittleSkin'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Try to request 'https://littleskin.cn/IceNoMC.json'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Cache file found (Length: 3 , Path: 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\d117f8465e833ba5c4bd5152568719f4110d9622' , Expire: 1589982044')
[2020-05-20 17:57:17] [IceNoMC INFO] Try to load from cache 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\d117f8465e833ba5c4bd5152568719f4110d9622'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Successfully load from cache
[2020-05-20 17:57:17] [IceNoMC DEBUG] Content: {}

[2020-05-20 17:57:17] [IceNoMC INFO] Both skin and cape not found.
[2020-05-20 17:57:17] [IceNoMC INFO] 3/7 Try to load profile from 'BlessingSkin'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Try to request 'http://skin.prinzeugen.net/IceNoMC.json'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Failed to request (Response Code: 404)
[2020-05-20 17:57:17] [IceNoMC INFO] Profile not found.
[2020-05-20 17:57:17] [IceNoMC INFO] 4/7 Try to load profile from 'ElyBy'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Try to request 'http://skinsystem.ely.by/textures/IceNoMC?version=2&minecraft_version=1.14.4'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Cache file found (Length: 0 , Path: 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\a2242fe09de4ac57cd65dcd1b86247f7487d735f' , Expire: 1589971244')
[2020-05-20 17:57:17] [IceNoMC INFO] Try to load from cache 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\a2242fe09de4ac57cd65dcd1b86247f7487d735f'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Successfully load from cache
[2020-05-20 17:57:17] [IceNoMC DEBUG] Content: 
[2020-05-20 17:57:17] [IceNoMC INFO] Profile not found.
[2020-05-20 17:57:17] [IceNoMC INFO] 5/7 Try to load profile from 'SkinMe'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Try to request 'http://www.skinme.cc/uniskin/IceNoMC.json'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Cache file found (Length: 37 , Path: 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\0d488552b3ffef4da5e56fa2b43ed5bcb6927675' , Expire: 1589968727')
[2020-05-20 17:57:17] [IceNoMC INFO] Try to load from cache 'D:\Documents\Downloads\1.14.4fabric整合V1.3\.minecraft\CustomSkinLoader\caches\0d488552b3ffef4da5e56fa2b43ed5bcb6927675'.
[2020-05-20 17:57:17] [IceNoMC DEBUG] Successfully load from cache
[2020-05-20 17:57:17] [IceNoMC DEBUG] Content: {"errno":404,"msg":"User not found."}
[2020-05-20 17:57:17] [IceNoMC INFO] Error 404: User not found.
[2020-05-20 17:57:17] [IceNoMC INFO] 6/7 Try to load profile from 'LocalSkin'.
[2020-05-20 17:57:17] [IceNoMC INFO] IceNoMC's profile loaded.
[2020-05-20 17:57:17] [IceNoMC INFO] (SkinUrl: (LOCAL_LEGACY)d36e8c6d85f2cbc30993294b9314ecfa6809607b,LocalSkin/skins/IceNoMC.png , Model: auto , CapeUrl: null  , Expiry: 1589968672)
[2020-05-20 17:57:17] [Client thread DEBUG] Loading type:SKIN
'''
m1, m2 = cslHandler(s)
print(m1)
print(m2)
