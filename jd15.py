import struct, json, os, pinyin, re
from unidecode import unidecode

try:
    os.mkdir("output")

except:
    pass

try:
    os.makedirs("input/jd15")

    print('The directories have been made.')
    
    input('Insert your ckd files in input/jd15 and then run the tool again to deserialize the tapes.')

except:
    pass

for files in os.listdir("input/jd15"):
    if files.endswith("_tml_dance.dtape.ckd"):
        a=open("input/jd15/"+files,"rb")
        print('deserializing '+files)
        dtape={}
        dtape["__class"]="Tape"
        dtapeclips=[]
        a.read(16)
        clips=struct.unpack('>I',a.read(4))[0]
        for clip in range(clips):
            a.read(4)
            classtype=a.read(4)
            if classtype==b'\x00\x00\x00\x6C' or classtype==b'\x00\x00\x00\x70':#moveclip
                move_id=struct.unpack('>I',a.read(4))[0]
                move_trackid=struct.unpack('>I',a.read(4))[0]
                move_isactive=struct.unpack('>I',a.read(4))[0]
                move_starttime=struct.unpack('>i',a.read(4))[0]
                move_duration=struct.unpack('>i',a.read(4))[0]
                move_file_len=struct.unpack('>I',a.read(4))[0]
                move_file=a.read(move_file_len).decode("utf-8")
                move_path_len=struct.unpack('>I',a.read(4))[0]
                move_path=a.read(move_path_len).decode("utf-8")
                a.read(8)
                move_goldmove=struct.unpack('>I',a.read(4))[0]
                move_coachid=struct.unpack('>I',a.read(4))[0]
                movetype=struct.unpack('>I',a.read(4))[0]
                move_color3=struct.unpack('>f',a.read(4))[0]
                move_color2=struct.unpack('>f',a.read(4))[0]
                move_color1=struct.unpack('>f',a.read(4))[0]
                move_color0=struct.unpack('>f',a.read(4))[0]
                a.read(4)
                a.read(8)
                scorescale1=struct.unpack('>f',a.read(4))[0]
                scoresmoothing1=struct.unpack('>f',a.read(4))[0]
                scoringmode1=struct.unpack('>f',a.read(4))[0]
                a.read(8)
                scorescale2=struct.unpack('>f',a.read(4))[0]
                scoresmoothing2=struct.unpack('>f',a.read(4))[0]
                scoringmode2=struct.unpack('>f',a.read(4))[0]
                a.read(8)
                scorescale3=struct.unpack('>f',a.read(4))[0]
                scoresmoothing3=struct.unpack('>f',a.read(4))[0]
                scoringmode3=struct.unpack('>f',a.read(4))[0]
                
                moveclip={
                "__class": "MotionClip",
                "Id": move_id,
                "TrackId": move_trackid,
                "IsActive": move_isactive,
                "StartTime": move_starttime,
                "Duration": move_duration,
                "ClassifierPath": move_path.replace("jd2015","maps")+move_file,
                "GoldMove": move_goldmove,
                "CoachId": move_coachid,
                "MoveType": movetype,
                "Color": [move_color0,move_color1,move_color2,move_color3],
                "MotionPlatformSpecifics": {
                    "X360": {
                        "__class": "MotionPlatformSpecific",
                        "ScoreScale": scorescale1,
                        "ScoreSmoothing": scoresmoothing1,
                        "ScoringMode": scoringmode1
                        },
                    "ORBIS": {
                        "__class": "MotionPlatformSpecific",
                        "ScoreScale": scorescale2,
                        "ScoreSmoothing": scoresmoothing2,
                        "ScoringMode": scoringmode2
                        },
                    "DURANGO": {
                        "__class": "MotionPlatformSpecific",
                        "ScoreScale": scorescale3,
                        "ScoreSmoothing": scoresmoothing3,
                        "ScoringMode": scoringmode3
                        }
                    }
                }
                dtapeclips.append(moveclip)

            elif classtype==b'\x00\x00\x00\x38':#pictoclip
                picto_id=struct.unpack('>I',a.read(4))[0]
                picto_trackid=struct.unpack('>I',a.read(4))[0]
                picto_isactive=struct.unpack('>I',a.read(4))[0]
                picto_starttime=struct.unpack('>i',a.read(4))[0]
                picto_duration=struct.unpack('>i',a.read(4))[0]
                picto_file_len=struct.unpack('>I',a.read(4))[0]
                picto_file=a.read(picto_file_len).decode("utf-8")
                picto_path_len=struct.unpack('>I',a.read(4))[0]
                picto_path=a.read(picto_path_len).decode("utf-8")
                a.read(8)
                picto_coachcount=struct.unpack('>I',a.read(4))[0]
                
                pictoclip={
                "__class": "PictogramClip",
                "Id": picto_id,
                "TrackId": picto_trackid,
                "IsActive": picto_isactive,
                "StartTime": picto_starttime,
                "Duration": picto_duration,
                "PictoPath": picto_path.replace("jd2015","maps")+picto_file,
                "CoachCount": picto_coachcount
                }
                dtapeclips.append(pictoclip)

            elif classtype==b'\x00\x00\x00\x1C':#goldeffectclip
                goldeffect_id=struct.unpack('>I',a.read(4))[0]
                goldeffect_trackid=struct.unpack('>I',a.read(4))[0]
                goldeffect_isactive=struct.unpack('>I',a.read(4))[0]
                goldeffect_starttime=struct.unpack('>i',a.read(4))[0]
                goldeffect_duration=struct.unpack('>i',a.read(4))[0]
                goldeffect_effecttype=struct.unpack('>I',a.read(4))[0]
                
                goldeffectclip={
                "__class": "GoldEffectClip",
                "Id": goldeffect_id,
                "TrackId":  goldeffect_trackid,
                "IsActive": goldeffect_isactive,
                "StartTime": goldeffect_starttime,
                "Duration": goldeffect_duration,
                "EffectType": goldeffect_effecttype
                }
                dtapeclips.append(goldeffectclip)
        
        dtape["Clips"]=dtapeclips
        a.read(8)
        tapeclock=struct.unpack('>I',a.read(4))[0]
        tapebarcount=struct.unpack('>I',a.read(4))[0]
        freeresourcesafterplay=struct.unpack('>I',a.read(4))[0]
        codename_len=struct.unpack('>I',a.read(4))[0]
        codename=a.read(codename_len).decode("utf-8")

        dtape["TapeClock"]=tapeclock
        dtape["TapeBarCount"]=tapebarcount
        dtape["FreeResourcesAfterPlay"]=freeresourcesafterplay
        dtape["MapName"]=codename
        dtape["SoundwichEvent"]=""

        outputdirectory='output/'+codename

        try:
            os.makedirs(outputdirectory)

        except:
            pass

        json.dump(dtape,open(outputdirectory+'/'+files,"w"))

    if files.endswith("_tml_karaoke.ktape.ckd"):
        b=open("input/jd15/"+files,"rb")
        print('deserializing '+files)
        codename=files.replace("_tml_karaoke.ktape.ckd","")
        ktape={}
        ktape["__class"]="Tape"
        ktapeclips=[]
        b.read(16)
        clips=struct.unpack('>I',b.read(4))[0]
        for clip in range(clips):
            b.read(4)
            classtype=b.read(4)
            if classtype==b'\x00\x00\x00\x50':#karaokeclip
                karaoke_id=struct.unpack('>I',b.read(4))[0]
                karaoke_trackid=struct.unpack('>I',b.read(4))[0]
                karaoke_isactive=struct.unpack('>I',b.read(4))[0]
                karaoke_starttime=struct.unpack('>i',b.read(4))[0]
                karaoke_duration=struct.unpack('>i',b.read(4))[0]
                karaoke_pitch=struct.unpack('>f',b.read(4))[0]
                karaoke_lyric_len=struct.unpack('>I',b.read(4))[0]
                karaoke_lyric=b.read(karaoke_lyric_len).decode("utf-8")
                karaoke_endofline=struct.unpack('>I',b.read(4))[0]
                karaoke_contenttype=struct.unpack('>I',b.read(4))[0]
                karaoke_starttimetolerance=struct.unpack('>I',b.read(4))[0]
                karaoke_endtimetolerance=struct.unpack('>I',b.read(4))[0]
                karaoke_semitonetolerance=struct.unpack('>f',b.read(4))[0]

                #convert chinese lyrics to pinyin
                if re.search(u'[\u4e00-\u9fff]',karaoke_lyric):
                    karaoke_lyric=pinyin.get(karaoke_lyric,format="strip",delimiter=" ")+" "

                karaoke_lyric=unidecode(karaoke_lyric)

                karaokeclip={
                "__class": "KaraokeClip",
                "Id": karaoke_id,
                "TrackId": karaoke_trackid,
                "IsActive": karaoke_isactive,
                "StartTime": karaoke_starttime,
                "Duration": karaoke_duration,
                "Pitch": karaoke_pitch,
                "Lyrics": karaoke_lyric,
                "IsEndOfLine": karaoke_endofline,
                "ContentType": karaoke_contenttype,
                "StartTimeTolerance": karaoke_starttimetolerance,
                "EndTimeTolerance": karaoke_endtimetolerance,
                "SemitoneTolerance": karaoke_semitonetolerance
                }
                ktapeclips.append(karaokeclip)
        
        ktape["Clips"]=ktapeclips

        ktape["TapeClock"]=0
        ktape["TapeBarCount"]=1
        ktape["FreeResourcesAfterPlay"]=0
        ktape["MapName"]=codename
        ktape["SoundwichEvent"]=""

        outputdirectory='output/'+codename

        try:
            os.makedirs(outputdirectory)

        except:
            pass

        json.dump(ktape,open(outputdirectory+'/'+files,"w"))

    if files.endswith("songdesc.tpl.ckd"):
        d=open("input/jd15/"+files,"rb")
        print('deserializing '+files)
        songdesc={}
        songdesc["__class"]="Actor_Template"
        songdesc["WIP"]=0
        songdesc["LOWUPDATE"]=0
        songdesc["UPDATE_LAYER"]=0
        songdesc["PROCEDURAL"]=0
        songdesc["STARTPAUSED"]=0
        songdesc["FORCEISENVIRONMENT"]=0

        songdesctemplate={}

        d.read(56)
        codename_len=struct.unpack('>I',d.read(4))[0]
        codename=d.read(codename_len).decode("utf-8")
        originaljdversion=struct.unpack('>I',d.read(4))[0]
        d.read(4)
        isalt=struct.unpack('>I',d.read(4))[0]
        if isalt==1:
            codenamealt_len=struct.unpack('>I',d.read(4))[0]
            codenamealt=d.read(codenamealt_len).decode("utf-8")
        quantity=struct.unpack('>I',d.read(4))[0]
        d.read(16)
        localeid=struct.unpack('>I',d.read(4))[0]
        d.read(32)
        if quantity==2:
            d.read(52)
        artist_len=struct.unpack('>I',d.read(4))[0]
        artist=d.read(artist_len).decode("utf-8")
        dancername_len=struct.unpack('>I',d.read(4))[0]
        dancername=d.read(dancername_len).decode("utf-8")
        title_len=struct.unpack('>I',d.read(4))[0]
        title=d.read(title_len).decode("utf-8")
        numcoach=struct.unpack('>I',d.read(4))[0]
        d.read(4)
        difficulty=struct.unpack('>I',d.read(4))[0]
        backgroundtype=struct.unpack('>I',d.read(4))[0]
        lyrictype=struct.unpack('>I',d.read(4))[0]
        if isalt!=1:
            d.read(20)
            previewentry=struct.unpack('>I',d.read(4))[0]
            d.read(12)
            previewloopstart=struct.unpack('>I',d.read(4))[0]
            previewloopend=struct.unpack('>I',d.read(4))[0]
            previewbeats={}#making a seperated json file for the musictrack to read proper preview beats
            previewbeats["previewEntry"]=previewentry
            previewbeats["previewLoopStart"]=previewloopstart
            previewbeats["previewLoopEnd"]=previewloopend
            json.dump(previewbeats,open('previewbeats.json',"w"))
        else:
            d.read(16)
            previewentry=struct.unpack('>I',d.read(4))[0]
            d.read(12)
            previewloopstart=struct.unpack('>I',d.read(4))[0]
            previewloopend=struct.unpack('>I',d.read(4))[0]
        d.read(8)
        lyriccolor3=struct.unpack('>f',d.read(4))[0]
        lyriccolor2=struct.unpack('>f',d.read(4))[0]
        lyriccolor1=struct.unpack('>f',d.read(4))[0]
        lyriccolor0=struct.unpack('>f',d.read(4))[0]

        #chinese converting for song & artist name
        if re.search(u'[\u4e00-\u9fff]',artist):
            artist=pinyin.get(artist,format="strip",delimiter=" ")+" "

        if re.search(u'[\u4e00-\u9fff]',title):
            title=pinyin.get(title,format="strip",delimiter=" ")+" "

        #generate phone texture urls
        codenamelow=codename.lower()
        coverphone="world/maps/"+codenamelow+"/menuart/textures/"+codenamelow+"_cover_phone.jpg"
        coach1phone="world/maps/"+codenamelow+"/menuart/textures/"+codenamelow+"_coach_1_phone.png"
        coach2phone="world/maps/"+codenamelow+"/menuart/textures/"+codenamelow+"_coach_2_phone.png"
        coach3phone="world/maps/"+codenamelow+"/menuart/textures/"+codenamelow+"_coach_3_phone.png"
        coach4phone="world/maps/"+codenamelow+"/menuart/textures/"+codenamelow+"_coach_4_phone.png"
        phoneimages={}
        phoneimages["cover"]=coverphone
        if numcoach>=1:
            phoneimages["coach1"]=coach1phone
        if numcoach>=2:
            phoneimages["coach2"]=coach2phone
        if numcoach>=3:
            phoneimages["coach3"]=coach3phone
        if numcoach>=4:
            phoneimages["coach4"]=coach4phone

        songdesctemplate["__class"]="JD_SongDescTemplate"
        songdesctemplate["MapName"]=codename
        songdesctemplate["JDVersion"]=2016
        songdesctemplate["OriginalJDVersion"]=originaljdversion
        if isalt==1:
            songdesctemplate["RelatedAlbums"]=codenamealt
        songdesctemplate["Artist"]=artist
        songdesctemplate["DancerName"]=dancername
        songdesctemplate["Title"]=title
        songdesctemplate["Credits"]=""
        songdesctemplate["PhoneImages"]=phoneimages
        songdesctemplate["NumCoach"]=numcoach
        songdesctemplate["MainCoach"]=-1
        songdesctemplate["Difficulty"]=difficulty
        songdesctemplate["SweatDifficulty"]=difficulty
        songdesctemplate["BackgroundType"]=backgroundtype
        songdesctemplate["LyricsType"]=lyrictype
        songdesctemplate["Energy"]=1
        songdesctemplate["Tags"]=["main"]
        songdesctemplate["Status"]=3
        songdesctemplate["LocaleID"]=localeid
        songdesctemplate["MojoValue"]=0
        songdesctemplate["CountInProgression"]=1
        defaultcolors={}
        defaultcolors["lyrics"]=[lyriccolor0,lyriccolor1,lyriccolor2,lyriccolor3]
        defaultcolors["theme"]=[1,1,1,1]
        songdesctemplate["DefaultColors"]=defaultcolors
        songdesctemplate["VideoPreviewPath"]=""
        components=[songdesctemplate]

        songdesc["COMPONENTS"]=components

        outputdirectory='output/'+codename

        try:
            os.makedirs(outputdirectory)

        except:
            pass

        json.dump(songdesc,open(outputdirectory+'/'+files,"w"))

    if files.endswith("_musictrack.tpl.ckd") or files.endswith("_musictrack.main_legacy.tpl.ckd"):
        c=open("input/jd15/"+files,"rb")
        print('deserializing '+files)
        musictrack={}
        musictrack["__class"]="Actor_Template"
        musictrack["WIP"]=0
        musictrack["LOWUPDATE"]=0
        musictrack["UPDATE_LAYER"]=0
        musictrack["PROCEDURAL"]=0
        musictrack["STARTPAUSED"]=0
        musictrack["FORCEISENVIRONMENT"]=0
        beats=[]
        signaturetape={}
        sectiontape={}
        signatureclips=[]
        sectionclips=[]
        c.read(64)
        markers=struct.unpack('>I',c.read(4))[0]
        for marker in range(markers):
            beat=struct.unpack('>I',c.read(4))[0]
            beats.append(beat)

        signatures=struct.unpack('>I',c.read(4))[0]
        for signature in range(signatures):
            c.read(4)
            signature_marker=struct.unpack('>I',c.read(4))[0]
            signature_beat=struct.unpack('>I',c.read(4))[0]
            signaturetape["__class"]="MusicSignature"
            signaturetape["marker"]=signature_marker
            signaturetape["beats"]=signature_beat
            signatureclips.append(signaturetape)

        sections=struct.unpack('>I',c.read(4))[0]
        for section in range(sections):
            c.read(4)
            section_marker=struct.unpack('>I',c.read(4))[0]
            sectiontype=struct.unpack('>I',c.read(4))[0]
            section_comment_len=struct.unpack('>I',c.read(4))[0]
            section_comment=c.read(section_comment_len).decode("utf-8")

            sectiontape["__class"]="MusicSection"
            sectiontape["marker"]=section_marker
            sectiontape["sectionType"]=sectiontype
            sectiontape["comment"]=section_comment
            sectionclips.append(sectiontape)

        #end of musictrack
        startbeat=struct.unpack('>i',c.read(4))[0]
        endbeat=struct.unpack('>I',c.read(4))[0]
        videostarttime=struct.unpack('>f',c.read(4))[0]
        volume=struct.unpack('>I',c.read(4))[0]
        audio_file_len=struct.unpack('>I',c.read(4))[0]
        audio_file=c.read(audio_file_len).decode("utf-8")
        audio_path_len=struct.unpack('>I',c.read(4))[0]
        audio_path=c.read(audio_path_len).decode("utf-8")
        c.read(12)

        codename=audio_file.replace(".wav","")

        structure={}
        structure["__class"]="MusicTrackStructure"
        structure["markers"]=beats
        structure["signatures"]=signatureclips
        structure["sections"]=sectionclips
        structure["startBeat"]=startbeat
        structure["endBeat"]=endbeat
        structure["videoStartTime"]=videostarttime
        try:
            previewvalues=json.load(open("previewbeats.json"))
            structure["previewEntry"]=previewvalues["previewEntry"]
            structure["previewLoopStart"]=previewvalues["previewLoopStart"]
            structure["previewLoopEnd"]=previewvalues["previewLoopEnd"]
        except FileNotFoundError:
            structure["previewEntry"]=25
            structure["previewLoopStart"]=50
            structure["previewLoopEnd"]=100
        structure["volume"]=volume

        mtdata={}
        mtdata["__class"]="MusicTrackData"
        mtdata["structure"]=structure
        mtdata["path"]=audio_path.replace("jd2015","maps")+audio_file
        mtdata["url"]="jmcs://jd-contents/"+codename+"/"+codename+".ogg"

        mttemplate={}

        mttemplate["__class"]="MusicTrackComponent_Template"
        mttemplate["trackData"]=mtdata

        components=[mttemplate]

        musictrack["COMPONENTS"]=components

        outputdirectory='output/'+codename

        try:
            os.makedirs(outputdirectory)

        except:
            pass

        json.dump(musictrack,open(outputdirectory+'/'+files,"w"))

    if files.endswith("_mainsequence.tape.ckd"):
        e=open("input/jd15/"+files,"rb")
        print('deserializing '+files)
        codename=files.replace("_mainsequence.tape.ckd","")
        cine={}
        cine["__class"]="Tape"
        cineclips=[]
        e.read(16)
        clips=struct.unpack('>I',e.read(4))[0]
        for clip in range(clips):
            e.read(4)
            classtype=e.read(4)
            if classtype==b'\x00\x00\x00\x40':#soundsetclip
                amb_id=struct.unpack('>I',e.read(4))[0]
                amb_trackid=struct.unpack('>I',e.read(4))[0]
                amb_isactive=struct.unpack('>I',e.read(4))[0]
                amb_starttime=struct.unpack('>i',e.read(4))[0]
                amb_duration=struct.unpack('>i',e.read(4))[0]
                amb_file_len=struct.unpack('>I',e.read(4))[0]
                amb_file=e.read(amb_file_len).decode("utf-8")
                amb_path_len=struct.unpack('>I',e.read(4))[0]
                amb_path=e.read(amb_path_len).decode("utf-8")
                e.read(4)
                soundchannel=struct.unpack('>I',e.read(4))[0]
                startoffset=struct.unpack('>I',e.read(4))[0]
                stopsonend=struct.unpack('>I',e.read(4))[0]
                accountedforduration=struct.unpack('>I',e.read(4))[0]
                
                soundsetclip={
                "__class": "SoundSetClip",
                "Id": amb_id,
                "TrackId": amb_trackid,
                "IsActive": amb_isactive,
                "StartTime": amb_starttime,
                "Duration": amb_duration,
                "SoundSetPath": amb_path.replace("jd2015","maps")+amb_file,
                "SoundChannel": soundchannel,
                "StartOffset": startoffset,
                "StopsOnEnd": stopsonend,
                "AccountedForDuration": accountedforduration
                }

                cineclips.append(soundsetclip)

            elif classtype==b'\x00\x00\x00\x38' or classtype==b'\x00\x00\x00\x48':#hideuiclip
                hideui_id=struct.unpack('>I',e.read(4))[0]
                hideui_trackid=struct.unpack('>I',e.read(4))[0]
                hideui_isactive=struct.unpack('>I',e.read(4))[0]
                hideui_starttime=struct.unpack('>i',e.read(4))[0]
                hideui_duration=struct.unpack('>i',e.read(4))[0]
                e.read(4)
                eventtype=struct.unpack('>I',e.read(4))[0]
                e.read(4)
                hideuiclip={
                "__class": "HideUserInterfaceClip",
                "Id": hideui_id,
                "TrackId": hideui_trackid,
                "IsActive": hideui_isactive,
                "StartTime": hideui_starttime,
                "Duration": hideui_duration,
                "EventType": eventtype,
                "CustomParam": ""
                }
                cineclips.append(hideuiclip)

            #I would do graph clips but it's too complicated to set up!!! If you insert a bunch of serialized maps in the input folder including a mainsequence tape, than it will not deserialize all of them. It will go by alphabetical order by filename.
        
        cine["Clips"]=cineclips

        cine["TapeClock"]=0
        cine["TapeBarCount"]=1
        cine["FreeResourcesAfterPlay"]=0
        cine["MapName"]=codename
        cine["SoundwichEvent"]=""

        outputdirectory='output/'+codename

        try:
            os.makedirs(outputdirectory)

        except:
            pass

        json.dump(cine,open(outputdirectory+'/'+files,"w"))

    if files.endswith(".stape.ckd"):
        f=open("input/jd15/"+files,"rb")
        print('deserializing '+files)
        stape={}
        stape["__class"]="Tape"
        stapeclips=[]
        f.read(16)
        clips=struct.unpack('>I',f.read(4))[0]
        for clip in range(clips):
            f.read(4)
            classtype=f.read(4)
            if classtype==b'\x00\x00\x00\x34':#stapeclip
                stape_id=struct.unpack('>I',f.read(4))[0]
                stape_trackid=struct.unpack('>I',f.read(4))[0]
                stape_isactive=struct.unpack('>I',f.read(4))[0]
                stape_starttime=struct.unpack('>i',f.read(4))[0]
                stape_duration=struct.unpack('>i',f.read(4))[0]
                stape_bpm=struct.unpack('>f',f.read(4))[0]
                stape_signature_len=struct.unpack('>I',f.read(4))[0]
                stape_signature=f.read(stape_signature_len).decode("utf-8")
                stape_guid_len=struct.unpack('>I',f.read(4))[0]
                stape_guid=f.read(stape_guid_len).decode("utf-8")
                
                slotclip={
                "__class": "SlotClip",
                "Id": stape_id,
                "TrackId": stape_trackid,
                "IsActive": stape_isactive,
                "StartTime": stape_starttime,
                "Duration": stape_duration,
                "Bpm": stape_bpm,
                "Signature": stape_signature,
                "Guid": stape_guid
                }
                stapeclips.append(slotclip)
        
        stape["Clips"]=stapeclips
        f.read(8)
        tapeclock=struct.unpack('>I',f.read(4))[0]
        tapebarcount=struct.unpack('>I',f.read(4))[0]
        freeresourcesafterplay=struct.unpack('>I',f.read(4))[0]
        codename_len=struct.unpack('>I',f.read(4))[0]
        codename=f.read(codename_len).decode("utf-8")

        stape["TapeClock"]=tapeclock
        stape["TapeBarCount"]=tapebarcount
        stape["FreeResourcesAfterPlay"]=freeresourcesafterplay
        stape["MapName"]=codename
        stape["SoundwichEvent"]=""

        outputdirectory='output/'+codename

        try:
            os.makedirs(outputdirectory)

        except:
            pass

        json.dump(stape,open(outputdirectory+'/'+files,"w"))