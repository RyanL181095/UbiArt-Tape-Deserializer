import struct, json, os, pinyin, re, random
from unidecode import unidecode

try:
    os.mkdir("output")

except:
    pass

try:
    os.makedirs("input/jd14")

    print('The directories have been made.')
    
    input('Insert your ckd files in input/jd14 and then run the tool again to deserialize the tapes.')

except:
    pass
    
for files in os.listdir("input/jd14"):
    if files.endswith("timeline.tpl.ckd"):
        a=open("input/jd14/"+files,"rb")
        print('deserializing '+files)
        dtape={}
        dtape["__class"]="Tape"
        dtapeclips=[]
        ktape={}
        ktape["__class"]="Tape"
        ktapeclips=[]
        a.read(56)#header
        codename_len=struct.unpack('>I',a.read(4))[0]
        codename=a.read(codename_len).decode("utf-8")
        codenamelow=codename.lower()
        a.read(28)#songgeneraldata

        #karaokescoringdata
        windowhop=struct.unpack('>I',a.read(4))[0]
        windowsize=struct.unpack('>I',a.read(4))[0]
        rmsthreshold=struct.unpack('>f',a.read(4))[0]
        rmstendencytoincrease=struct.unpack('>f',a.read(4))[0]
        slidingmeanvariationthreshold=struct.unpack('>f',a.read(4))[0]
        yinpitchthreshold=struct.unpack('>f',a.read(4))[0]
        pitchlowerbound=struct.unpack('>f',a.read(4))[0]
        pitchupperbound=struct.unpack('>f',a.read(4))[0]
        historyspan=struct.unpack('>I',a.read(4))[0]
        slidingmeanwindowsize=struct.unpack('>I',a.read(4))[0]
        rmstendencytodecrease=struct.unpack('>f',a.read(4))[0]
        nopitchscoring=struct.unpack('>f',a.read(4))[0]

        metainfo_id=random.randint(10000000, 99999999)
        metainfo=[{
            "__class": "KaraokeMetaInfo",
            "id": metainfo_id,
            "WindowSize": windowsize,
            "WindowHop": windowhop,
            "RMSThreshold": rmsthreshold,
            "RMSTendencyToIncrease": rmstendencytoincrease,
            "RMSTendencyToDecrease": rmstendencytodecrease,
            "YinPitchTreshold": yinpitchthreshold,
            "PitchLowerBound": pitchlowerbound,
            "PitchUpperBound": pitchupperbound,
            "HistorySpan": historyspan,
            "SlidingMeanWindowSize": slidingmeanwindowsize,
            "SlidingMeanVariationThreshold": slidingmeanvariationthreshold,
            "NoPitchScoring": nopitchscoring,
            "GraphicsPitchMeanWindow": 10
        }]

        signalannotation=struct.unpack('>I',a.read(4))[0]
        for vect in range(signalannotation):
            a.read(44)

        pictos=struct.unpack('>I',a.read(4))[0]
        picto_id=random.randint(10000000, 99999999)
        picto_trackid=random.randint(10000000, 99999999)
        for picto in range(pictos):
            a.read(4)
            picto_position=struct.unpack('>f',a.read(4))[0]
            pictoname_len=struct.unpack('>I',a.read(4))[0]
            pictoname=a.read(pictoname_len).decode("utf-8")
            a.read(4)
            pictopath_len=struct.unpack('>I',a.read(4))[0]
            pictopath=a.read(pictopath_len).decode("utf-8")
            pictofile_len=struct.unpack('>I',a.read(4))[0]
            pictofile=a.read(pictofile_len).decode("utf-8")
            a.read(8)

            picto_starttime=round(picto_position*24)

            pictoclip={
            "__class": "PictogramClip",
            "Id": picto_id,
            "TrackId": picto_trackid,
            "IsActive": 1,
            "StartTime": picto_starttime,
            "Duration": 24,
            "PictoPath": pictopath.replace("jd5","maps")+pictofile,
            "CoachCount": 4294967295
            }

            dtapeclips.append(pictoclip)

            picto_id+=1

        moves=struct.unpack('>I',a.read(4))[0]
        move_id=random.randint(10000000, 99999999)
        move_trackid=random.randint(10000000, 99999999)
        for move in range(moves):
            a.read(4)
            movename_len=struct.unpack('>I',a.read(4))[0]
            movename=a.read(movename_len).decode("utf-8")
            move_layerid=struct.unpack('>I',a.read(4))[0]
            movepath_len=struct.unpack('>I',a.read(4))[0]
            movepath=a.read(movepath_len).decode("utf-8")
            movefile_len=struct.unpack('>I',a.read(4))[0]
            movefile=a.read(movefile_len).decode("utf-8")
            a.read(8)
            move_startposition=struct.unpack('>f',a.read(4))[0]
            move_stopposition=struct.unpack('>f',a.read(4))[0]
            move_goldmove=struct.unpack('>I',a.read(4))[0]
            a.read(12)

            move_starttime=round(move_startposition*24)
            move_duration=round(move_stopposition*24)-move_starttime

            

            #for coachid, you have to manually change the values so that it can register the correct coach for the timeline.

            #list of coachids:
            #coachid: 0 = coach 1
            #coachid: 1 = coach 2
            #coachid: 2 = coach 3
            #coachid: 3 = coach 4

            movetape={
            "__class": "MotionClip",
            "Id": move_id,
            "TrackId": move_trackid,
            "IsActive": 1,
            "StartTime": move_starttime,
            "Duration": move_duration,
            "ClassifierPath": movepath.replace("jd5","maps")+movefile,
            "GoldMove": move_goldmove,
            "CoachId": move_layerid,
            "MoveType": 0,
            "Color": [1, 1, 1, 1],
            "MotionPlatformSpecifics": {
                "X360": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "ScoringMode": 0
                },
                "ORBIS": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "ScoringMode": 0
                },
                "DURANGO": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "ScoringMode": 0
                }
            }
            }

            dtapeclips.append(movetape)

            move_id+=1

        kinectmoves=struct.unpack('>I',a.read(4))[0]
        kinectmove_id=random.randint(10000000, 99999999)
        kinectmove_trackid=random.randint(10000000, 99999999)
        for kinectmove in range(kinectmoves):
            a.read(4)
            movename_len=struct.unpack('>I',a.read(4))[0]
            movename=a.read(movename_len).decode("utf-8")
            move_layerid=struct.unpack('>I',a.read(4))[0]
            movepath_len=struct.unpack('>I',a.read(4))[0]
            movepath=a.read(movepath_len).decode("utf-8")
            movefile_len=struct.unpack('>I',a.read(4))[0]
            movefile=a.read(movefile_len).decode("utf-8")
            a.read(8)
            move_startposition=struct.unpack('>f',a.read(4))[0]
            move_stopposition=struct.unpack('>f',a.read(4))[0]
            move_goldmove=struct.unpack('>I',a.read(4))[0]
            a.read(12)

            move_starttime=round(move_startposition*24)
            move_duration=round(move_stopposition*24)-move_starttime

            #for coachid, you have to manually change the values so that it can register the correct coach for the timeline.

            #list of coachids:
            #coachid: 0 = coach 1
            #coachid: 1 = coach 2
            #coachid: 2 = coach 3
            #coachid: 3 = coach 4

            kinectmovetape={
            "__class": "MotionClip",
            "Id": kinectmove_id,
            "TrackId": kinectmove_trackid,
            "IsActive": 1,
            "StartTime": move_starttime,
            "Duration": move_duration,
            "ClassifierPath": movepath.replace("jd5","maps")+movefile,
            "GoldMove": move_goldmove,
            "CoachId": move_layerid,
            "MoveType": 0,
            "Color": [1, 1, 1, 1],
            "MotionPlatformSpecifics": {
                "X360": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "ScoringMode": 0
                },
                "ORBIS": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "ScoringMode": 0
                },
                "DURANGO": {
                    "__class": "MotionPlatformSpecific",
                    "ScoreScale": 1,
                    "ScoreSmoothing": 0,
                    "ScoringMode": 0
                }
            }
            }

            #if you want to decrypt kinect tapes, you can remove '#' beside dtapeclips.append
            #dtapeclips.append(kinectmovetape)

            kinectmove_id+=1

        lyrics=struct.unpack('>I',a.read(4))[0]
        lyric_id=random.randint(10000000, 99999999)
        lyric_trackid=random.randint(10000000, 99999999)
        for lyric in range(lyrics):
            a.read(4)
            lyrictext_len=struct.unpack('>I',a.read(4))[0]
            lyrictext=a.read(lyrictext_len).decode("utf-8")
            a.read(4)
            lyric_lineend=struct.unpack('>I',a.read(4))[0]
            lyric_startposition=struct.unpack('>f',a.read(4))[0]
            lyric_stopposition=struct.unpack('>f',a.read(4))[0]

            lyric_starttime=round(lyric_startposition*24)
            lyric_duration=round(lyric_stopposition*24)-lyric_starttime

            if re.search(u'[\u4e00-\u9fff]',lyrictext):
                lyrictext=pinyin.get(lyrictext,format="strip",delimiter=" ")+" "

            lyrictext=unidecode(lyrictext)

            lyrictape={
            "__class": "KaraokeClip",
            "Id": lyric_id,
            "TrackId": lyric_trackid,
            "IsActive": 1,
            "StartTime": lyric_starttime,
            "Duration": lyric_duration,
            "Pitch": 8.661958,
            "Lyrics": lyrictext,
            "IsEndOfLine": lyric_lineend,
            "ContentType": 1,
            "StartTimeTolerance": 4,
            "EndTimeTolerance": 4,
            "SemitoneTolerance": 6
            }

            ktapeclips.append(lyrictape)

            lyric_id+=1

        blocks=struct.unpack('>I',a.read(4))[0]
        goldmove_id=random.randint(10000000, 99999999)
        goldmove_trackid=random.randint(10000000, 99999999)
        for block in range(blocks):
            block_classtype=struct.unpack('>I',a.read(4))[0]
            block_useless=struct.unpack('>I',a.read(4))[0]
            block_uselessname=a.read(block_useless)
            block_startposition=struct.unpack('>f',a.read(4))[0]
            block_stopposition=struct.unpack('>f',a.read(4))[0]
            block_layerid=struct.unpack('>I',a.read(4))[0]
            blockname_len=struct.unpack('>I',a.read(4))[0]
            blockname=a.read(blockname_len).decode("utf-8")
            block_color1=struct.unpack('>B',a.read(1))[0]
            block_color2=struct.unpack('>B',a.read(1))[0]
            block_color3=struct.unpack('>B',a.read(1))[0]
            block_color4=struct.unpack('>B',a.read(1))[0]

            goldmove_starttime=round(block_startposition*24)

            if blockname=="goldmove":
                a.read(12)
                goldmovetext_len=struct.unpack('>I',a.read(4))[0]
                goldmovetext=a.read(goldmovetext_len).decode("utf-8")
                goldeffecttape={
                "__class": "GoldEffectClip",
                "Id": goldmove_id,
                "TrackId": goldmove_trackid,
                "IsActive": 1,
                "StartTime": goldmove_starttime+24,
                "Duration": 24,
                "EffectType": 1
                }

                dtapeclips.append(goldeffecttape)

                goldmove_id+=1

            if blockname=="goldmovecascade":
                endofcascade=a.read(4)
                if endofcascade==b'\x00\x00\x00\x01':
                    a.read(8)
                    goldmovetext_len=struct.unpack('>I',a.read(4))[0]
                    goldmovetext=a.read(goldmovetext_len).decode("utf-8")
                elif endofcascade==b'\x00\x00\x00\x00':
                    pass

                goldeffecttape={
                "__class": "GoldEffectClip",
                "Id": goldmove_id,
                "TrackId": goldmove_trackid,
                "IsActive": 1,
                "StartTime": goldmove_starttime+24,
                "Duration": 24,
                "EffectType": 2
                }

                dtapeclips.append(goldeffecttape)

                goldmove_id+=1
            
            if blockname=="karaokescoring":
                a.read(4)
            if blockname=="eventdelayeve":
                a.read(193)
            if blockname=="event_fadingvisual":
                a.read(148)
            if blockname=="tag":
                a.read(63)
            if blockname=="eventmultieve":
                a.read(103)
            if blockname=="playsnd":
                a.read(35)
            if blockname=="event_fadingmaterial":
                a.read(366)
            if blockname=="bpm":
                a.read(16)

        dtape["Clips"]=dtapeclips
        dtape["TapeClock"]=0
        dtape["TapeBarCount"]=1
        dtape["FreeResourcesAfterPlay"]=0
        dtape["MapName"]=codename
        dtape["SoundwichEvent"]=""

        ktape["Clips"]=ktapeclips
        ktape["MetaInfos"]=metainfo
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

        json.dump(dtape,open(outputdirectory+'/'+codenamelow+"_tml_dance.dtape.ckd","w"))
        json.dump(ktape,open(outputdirectory+'/'+codenamelow+"_tml_karaoke.ktape.ckd","w"))

    if files.endswith("songdesc.tpl.ckd"):
        b=open("input/jd14/"+files,"rb")
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

        b.read(56)
        codename_len=struct.unpack('>I',b.read(4))[0]
        codename=b.read(codename_len).decode("utf-8")
        originaljdversion=struct.unpack('>I',b.read(4))[0]
        isalt=struct.unpack('>I',b.read(4))[0]
        if isalt==1:
            codenamealt_len=struct.unpack('>I',b.read(4))[0]
            codenamealt=b.read(codenamealt_len).decode("utf-8")
        quantity=struct.unpack('>I',b.read(4))[0]
        if quantity==1 or quantity==2:
            for x in range(quantity):
                    b.read(44)
        if quantity==3:
            b.read(48)
            uselessshit=struct.unpack('>I',b.read(4))[0]
            if uselessshit==1:
                b.read(120)
            else:
                b.read(80)
        artist_len=struct.unpack('>I',b.read(4))[0]
        artist=b.read(artist_len).decode("utf-8")
        title_len=struct.unpack('>I',b.read(4))[0]
        title=b.read(title_len).decode("utf-8")
        numcoach=struct.unpack('>I',b.read(4))[0]
        difficulty=struct.unpack('>I',b.read(4))[0]
        if isalt!=1:
            b.read(20)
            previewentry=struct.unpack('>I',b.read(4))[0]
            b.read(12)
            previewloopstart=struct.unpack('>I',b.read(4))[0]
            previewloopend=struct.unpack('>I',b.read(4))[0]
            previewbeats={}#making a seperated json file for the musictrack to read proper preview beats
            previewbeats["previewEntry"]=previewentry
            previewbeats["previewLoopStart"]=previewloopstart
            previewbeats["previewLoopEnd"]=previewloopend
            json.dump(previewbeats,open('previewbeats.json',"w"))
            b.read(8)
        else:
            b.read(20)
            previewentry=struct.unpack('>I',b.read(4))[0]
            b.read(12)
            previewloopstart=struct.unpack('>I',b.read(4))[0]
            previewloopend=struct.unpack('>I',b.read(4))[0]
            previewbeats={}
            previewbeats["previewEntry"]=previewentry
            previewbeats["previewLoopStart"]=previewloopstart
            previewbeats["previewLoopEnd"]=previewloopend
            json.dump(previewbeats,open('previewbeats.json',"w"))
        lyriccolor3=struct.unpack('>f',b.read(4))[0]
        lyriccolor2=struct.unpack('>f',b.read(4))[0]
        lyriccolor1=struct.unpack('>f',b.read(4))[0]
        lyriccolor0=struct.unpack('>f',b.read(4))[0]

        #japan converting for song & artist name
        if re.search(u'[\u4e00-\u9fff]',artist):
            artist=pinyin.get(artist,format="strip",delimiter=" ")+" "

        artist=unidecode(artist)

        if re.search(u'[\u4e00-\u9fff]',title):
            title=pinyin.get(title,format="strip",delimiter=" ")+" "

        title=unidecode(title)

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
        songdesctemplate["DancerName"]="Unknown Dancer"
        songdesctemplate["Title"]=title
        songdesctemplate["Credits"]=""
        songdesctemplate["PhoneImages"]=phoneimages
        songdesctemplate["NumCoach"]=numcoach
        songdesctemplate["MainCoach"]=-1
        songdesctemplate["Difficulty"]=difficulty
        songdesctemplate["SweatDifficulty"]=difficulty
        songdesctemplate["BackgroundType"]=0
        songdesctemplate["LyricsType"]=0
        songdesctemplate["Energy"]=1
        songdesctemplate["Tags"]=["main"]
        songdesctemplate["Status"]=3
        songdesctemplate["LocaleID"]=4294967295
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

    if files.endswith("_musictrack.tpl.ckd"):
        c=open("input/jd14/"+files,"rb")
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
        audio_path_len=struct.unpack('>I',c.read(4))[0]
        audio_path=c.read(audio_path_len).decode("utf-8")
        audio_file_len=struct.unpack('>I',c.read(4))[0]
        audio_file=c.read(audio_file_len).decode("utf-8")
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
        structure["volume"]=0

        mtdata={}
        mtdata["__class"]="MusicTrackData"
        mtdata["structure"]=structure
        mtdata["path"]=audio_path.replace("jd5","maps")+audio_file
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
        d=open("input/jd14/"+files,"rb")
        print('deserializing '+files)
        codename=files.replace("_mainsequence.tape.ckd","")
        cine={}
        cine["__class"]="Tape"
        cineclips=[]
        d.read(16)
        clips=struct.unpack('>I',d.read(4))[0]
        for clip in range(clips):
            d.read(4)
            classtype=d.read(4)
            if classtype==b'\x00\x00\x00\x88':#soundsetclip
                amb_id=struct.unpack('>I',d.read(4))[0]
                amb_trackid=struct.unpack('>I',d.read(4))[0]
                amb_isactive=struct.unpack('>I',d.read(4))[0]
                amb_starttime=struct.unpack('>i',d.read(4))[0]
                amb_duration=struct.unpack('>i',d.read(4))[0]
                amb_path_len=struct.unpack('>I',d.read(4))[0]
                amb_path=d.read(amb_path_len).decode("utf-8")
                amb_file_len=struct.unpack('>I',d.read(4))[0]
                amb_file=d.read(amb_file_len).decode("utf-8")
                
                soundsetclip={
                "__class": "SoundSetClip",
                "Id": amb_id,
                "TrackId": amb_trackid,
                "IsActive": amb_isactive,
                "StartTime": amb_starttime,
                "Duration": amb_duration,
                "SoundSetPath": amb_path.replace("jd5","maps")+amb_file,
                "SoundChannel": 0,
                "StartOffset": 0,
                "StopsOnEnd": 0,
                "AccountedForDuration": 0
                }

                cineclips.append(soundsetclip)

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