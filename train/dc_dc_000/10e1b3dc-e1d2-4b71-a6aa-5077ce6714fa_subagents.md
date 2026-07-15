> DEVELOPER

Read the YouTube auto-caption transcript at `/tmp/ostris-ltx/transcript.txt`. It's Ostris's tutorial "How to Train a LTX-2.3 Character LoRA with AI Toolkit" — he trains a character LoRA of himself on LTX 2.3, and this is also the recipe behind his George Costanza / Seinfeld LoRA.

Extract every concrete training setting, parameter, value, and recommendation he gives. Auto-captions have no punctuation and may mangle technical terms (e.g. "Lora" "rank" "learning rate" "ARA" "AI toolkit" "Comfy") — use judgment.

Produce a tight markdown report with these sections:
1. **Dataset** — clip count, length, resolution, captioning approach, any prep steps
2. **Model / base** — exact model name, where to download
3. **Training config** — rank, alpha, learning rate, scheduler, optimizer, steps, batch size, gradient accumulation, timestep schedule, anything else numerical
4. **Hardware / runtime** — GPU, VRAM, training time, memory tricks (ARA, quantization, caching)
5. **Sampling during training** — sample prompts/cadence, what to look for
6. **Inference** — how he generates with the trained LoRA (ComfyUI workflow, weight, etc.)
7. **Tips / gotchas he calls out** — anything he explicitly warns about

For every value, quote the surrounding phrase so I can sanity-check. If a section has no info, write "not covered." Be terse — no preamble, no "great question," just the report. Under 600 words.

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /tmp/ostris-ltx/transcript.txt && ls -la /tmp/ostris-ltx/",
  "description": "Check transcript size"
}
```

> TOOL

tool_result Bash
```
0 /tmp/ostris-ltx/transcript.txt
total 456
drwxr-xr-x    4 user_c042661f  wheel     128 May 13 11:50 .
drwxrwxrwt  238 root          wheel    7616 May 13 11:50 ..
-rw-r--r--@   1 user_c042661f  wheel  144791 May 13 11:50 ostris.en.srt
-rw-r--r--@   1 user_c042661f  wheel   85545 May 13 11:50 transcript.txt
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/transcript.txt"
}
```

> TOOL

tool_result Read
```
File content (27836 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/transcript.txt",
  "limit": 800
}
```

> TOOL

tool_result Read
```
File content (27836 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/transcript.txt",
  "limit": 500
}
```

> TOOL

tool_result Read
```
File content (27836 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/transcript.txt",
  "offset": 1,
  "limit": 400
}
```

> TOOL

tool_result Read
```
File content (27836 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -c /tmp/ostris-ltx/transcript.txt && wc -w /tmp/ostris-ltx/transcript.txt",
  "description": "Get character and word count"
}
```

> TOOL

tool_result Bash
```
85545 /tmp/ostris-ltx/transcript.txt
   16871 /tmp/ostris-ltx/transcript.txt
```

> AGENT

The file has no newlines (single huge line). Let me read in chunks.

> TOOL

tool_use Bash
```json
{
  "command": "fold -w 200 /tmp/ostris-ltx/transcript.txt > /tmp/ostris-ltx/transcript_wrapped.txt && wc -l /tmp/ostris-ltx/transcript_wrapped.txt",
  "description": "Wrap transcript to lines"
}
```

> TOOL

tool_result Bash
```
427 /tmp/ostris-ltx/transcript_wrapped.txt
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/transcript_wrapped.txt",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	Hey guys, welcome back. I am Ostress. Hey guys, welcome back. I am Ostress. Today we are going to train an LTX 2.3 Today we are going to train an LTX 2.3 Today we are going to train an LTX 2.3 charact
2	er Laura. So, you're probably character Laura. So, you're probably character Laura. So, you're probably noticing something a little different noticing something a little different noticing something a
3	 little different here. Most of my videos, we zoom in on a here. Most of my videos, we zoom in on a here. Most of my videos, we zoom in on a blank screen on my monitor in front of blank screen on my m
4	onitor in front of blank screen on my monitor in front of me, and I am just an ethereal voice me, and I am just an ethereal voice me, and I am just an ethereal voice talking in the background. But tod
5	ay, we talking in the background. But today, we talking in the background. But today, we need some content. We need something to need some content. We need something to need some content. We need some
6	thing to train on. We need a character to train train on. We need a character to train train on. We need a character to train on. And unfortunately, it's really hard on. And unfortunately, it's really
7	 hard on. And unfortunately, it's really hard to get rights to the IP of a character. to get rights to the IP of a character. to get rights to the IP of a character. However, I have rights to the IP o
8	f one However, I have rights to the IP of one However, I have rights to the IP of one character, character, character, this guy. So, I'm going to start out this guy. So, I'm going to start out this gu
9	y. So, I'm going to start out with this video. This video is going to with this video. This video is going to with this video. This video is going to be the exact video I use to train the be the exact
10	 video I use to train the be the exact video I use to train the character Laura. We're going to go character Laura. We're going to go character Laura. We're going to go through, we're going to cut out
11	 scenes through, we're going to cut out scenes through, we're going to cut out scenes from this video, cut out my little from this video, cut out my little from this video, cut out my little pieces of
12	 text that I do, and we are pieces of text that I do, and we are pieces of text that I do, and we are going to train an LTX 2.3 Laura on this. going to train an LTX 2.3 Laura on this. going to train a
13	n LTX 2.3 Laura on this. So, we should be able to generate all of So, we should be able to generate all of So, we should be able to generate all of this with our Laura. I'm going to burn this with our
14	 Laura. I'm going to burn this with our Laura. I'm going to burn in the background. I'm going to burn in in the background. I'm going to burn in in the background. I'm going to burn in my clothes. I'm
15	 going to burn in my face my clothes. I'm going to burn in my face my clothes. I'm going to burn in my face and my scruffy facial hair. Everything and my scruffy facial hair. Everything and my scruffy
16	 facial hair. Everything about this whole essence is going to be about this whole essence is going to be about this whole essence is going to be burned into the Laura. So then I, you, burned into the 
17	Laura. So then I, you, burned into the Laura. So then I, you, whoever can just sit here and generate whoever can just sit here and generate whoever can just sit here and generate your own ostress cont
18	ent. To get your own ostress content. To get your own ostress content. To get started, I have to make a lot of started, I have to make a lot of started, I have to make a lot of expressions. I have to 
19	talk kind of slow expressions. I have to talk kind of slow expressions. I have to talk kind of slow at points because we want to be able to at points because we want to be able to at points because we
20	 want to be able to chop it up where I'm being very chop it up where I'm being very chop it up where I'm being very introspective and we I want to be introspective and we I want to be introspective an
21	d we I want to be excited on some things. LTX 2.3 is going excited on some things. LTX 2.3 is going excited on some things. LTX 2.3 is going to learn the voice. It's going to learn to learn the voice.
22	 It's going to learn to learn the voice. It's going to learn how I talk. It's going to learn the how I talk. It's going to learn the how I talk. It's going to learn the inflections of my voice. It's g
23	oing to inflections of my voice. It's going to inflections of my voice. It's going to learn the clothing I wear. It's going to learn the clothing I wear. It's going to learn the clothing I wear. It's 
24	going to learn everything about me. If we can learn everything about me. If we can learn everything about me. If we can chop all of this up properly. Let's just chop all of this up properly. Let's jus
25	t chop all of this up properly. Let's just get started. I'm going to take all this. get started. I'm going to take all this. get started. I'm going to take all this. We're going to pack it down. Let's
26	 hop We're going to pack it down. Let's hop We're going to pack it down. Let's hop over into KDEN Live. It's open source over into KDEN Live. It's open source over into KDEN Live. It's open source sof
27	tware. And from there, we're going to software. And from there, we're going to software. And from there, we're going to chop this up into little pieces. and chop this up into little pieces. and chop t
28	his up into little pieces. and we're going to build our data set so we're going to build our data set so we're going to build our data set so that we can train our own ostress that we can train our ow
29	n ostress that we can train our own ostress character Laura. Okay, I have KD and character Laura. Okay, I have KD and character Laura. Okay, I have KD and live pulled up. I'll put a link of this live 
30	pulled up. I'll put a link of this live pulled up. I'll put a link of this in the description in the description in the description that way you guys can see it. Let's just that way you guys can see i
31	t. Let's just that way you guys can see it. Let's just drop in our clip here. drop in our clip here. drop in our clip here. Okay, it immediately asks, do we want to Okay, it immediately asks, do we wa
32	nt to Okay, it immediately asks, do we want to switch? Yes, we do. This was recorded at switch? Yes, we do. This was recorded at switch? Yes, we do. This was recorded at 1440. 1440. 1440. All right, t
33	here wasn't audio. Let's All right, there wasn't audio. Let's All right, there wasn't audio. Let's drag that back in. Sometimes if you drag that back in. Sometimes if you drag that back in. Sometimes 
34	if you don't see the audio track, there was no don't see the audio track, there was no don't see the audio track, there was no audio. I'm not sure why that happened. audio. I'm not sure why that happe
35	ned. audio. I'm not sure why that happened. So, we'll just kind of browse through So, we'll just kind of browse through So, we'll just kind of browse through here and see what we can come up with. her
36	e and see what we can come up with. here and see what we can come up with. The intro. Hey guys, welcome back. I am The intro. Hey guys, welcome back. I am The intro. Hey guys, welcome back. I am ostro
37	us. Today, we are going to train an ostrous. Today, we are going to train an ostrous. Today, we are going to train an LTX 2.3 character Laura. Perfect. So, I LTX 2.3 character Laura. Perfect. So, I LT
38	X 2.3 character Laura. Perfect. So, I just want to go through and trim this just want to go through and trim this just want to go through and trim this up. We want it where back. I am ostous. So, We w
39	ant it where back. I am ostous. So, we can cut it out right here. So, that's we can cut it out right here. So, that's we can cut it out right here. So, that's going to put us about 4 seconds. We want 
40	going to put us about 4 seconds. We want going to put us about 4 seconds. We want to do it where I'm not midway through a to do it where I'm not midway through a to do it where I'm not midway through 
41	a word. So, I have like a whole sentence word. So, I have like a whole sentence word. So, I have like a whole sentence here or at least at a stopping point. here or at least at a stopping point. here 
42	or at least at a stopping point. Hey guys, welcome back. I am ostrous. Hey guys, welcome back. I am ostrous. Hey guys, welcome back. I am ostrous. Boom. And we'll do it to there. So, all Boom. And we'
43	ll do it to there. So, all Boom. And we'll do it to there. So, all we got to do is drag this blue line to we got to do is drag this blue line to we got to do is drag this blue line to there. Then I co
44	me up here and I click there. Then I come up here and I click there. Then I come up here and I click file and then we do render. file and then we do render. file and then we do render. So, we're going
45	 to do it to So, we're going to do it to So, we're going to do it to ostress_0000001. Uh, right here, it's important. Select Uh, right here, it's important. Select selected zone. See, you can tell the
46	 selected zone. See, you can tell the selected zone. See, you can tell the time changes there when we go from full time changes there when we go from full time changes there when we go from full proje
47	ct to selected zone. And that's project to selected zone. And that's project to selected zone. And that's just going to be our blue area here. just going to be our blue area here. just going to be our
48	 blue area here. So, then all of this is fine. Make sure So, then all of this is fine. Make sure So, then all of this is fine. Make sure we have audio we have audio we have audio render to file. And t
49	hat's our first clip. So, I'm just And that's our first clip. So, I'm just going to do that a bunch. I'll kind of going to do that a bunch. I'll kind of going to do that a bunch. I'll kind of speed th
50	rough that so you don't have to speed through that so you don't have to speed through that so you don't have to watch all the clips. And let's get our watch all the clips. And let's get our watch all 
51	the clips. And let's get our training data set. So, we have 19 videos. I just chopped up So, we have 19 videos. I just chopped up everything you guys just watched. We everything you guys just watched.
52	 We everything you guys just watched. We broke it up into little pieces. Uh, the broke it up into little pieces. Uh, the broke it up into little pieces. Uh, the pieces are in between, you know, two 3 
53	pieces are in between, you know, two 3 pieces are in between, you know, two 3 seconds up to about 8, eight and a half, seconds up to about 8, eight and a half, seconds up to about 8, eight and a half,
54	 I think, which all should be fine to I think, which all should be fine to I think, which all should be fine to train locally. So the next step, let's train locally. So the next step, let's train loca
55	lly. So the next step, let's go to AI toolkit. Let's get started. go to AI toolkit. Let's get started. go to AI toolkit. Let's get started. Okay, I'm going to pop over to Runpod. Okay, I'm going to po
56	p over to Runpod. Okay, I'm going to pop over to Runpod. I'm going to do this on RunPod. You can I'm going to do this on RunPod. You can I'm going to do this on RunPod. You can train this locally. You
57	 can train this train this locally. You can train this train this locally. You can train this on a 5090 at home doing full layer on a 5090 at home doing full layer on a 5090 at home doing full layer o
58	ffloading. I'll show you guys how to do offloading. I'll show you guys how to do offloading. I'll show you guys how to do that. Uh but just for speed and that. Uh but just for speed and that. Uh but j
59	ust for speed and everything. I'm going to do Runpod. I'll everything. I'm going to do Runpod. I'll everything. I'm going to do Runpod. I'll post a link in the description of how to post a link in the
60	 description of how to post a link in the description of how to set all this up. I have a whole video on set all this up. I have a whole video on set all this up. I have a whole video on how to use Ru
61	nOD. And if you're going to how to use RunOD. And if you're going to how to use RunOD. And if you're going to sign up for RunPod, use my affiliate sign up for RunPod, use my affiliate sign up for RunP
62	od, use my affiliate link. That kind of helps me out so that link. That kind of helps me out so that link. That kind of helps me out so that I can train videos like this. uh gives I can train videos l
63	ike this. uh gives I can train videos like this. uh gives me some credits for this. So, I'm going me some credits for this. So, I'm going me some credits for this. So, I'm going to use an RTX Pro. So,
64	 let's go over here. First thing I So, let's go over here. First thing I have to do is I have to build the data have to do is I have to build the data have to do is I have to build the data set on our
65	 brand new pod. New data set. set on our brand new pod. New data set. set on our brand new pod. New data set. We're just going to name this Austri. We're just going to name this Austri. We're just goi
66	ng to name this Austri. So, now I'm just going to drag and drop So, now I'm just going to drag and drop So, now I'm just going to drag and drop these videos over. Oh, and you guys get these videos ove
67	r. Oh, and you guys get these videos over. Oh, and you guys get to see the new drag and drop uploader. to see the new drag and drop uploader. to see the new drag and drop uploader. Works significantly
68	 better doing one Works significantly better doing one Works significantly better doing one video at a time. video at a time. video at a time. Much better. Much better. Much better. I know that needed
69	 improvement. A lot of I know that needed improvement. A lot of I know that needed improvement. A lot of people complained. That should solve the people complained. That should solve the people compla
70	ined. That should solve the issues. Let me know if you still have issues. Let me know if you still have issues. Let me know if you still have problems. So, now what we got to do here problems. So, now
71	 what we got to do here problems. So, now what we got to do here is go through the videos and caption is go through the videos and caption is go through the videos and caption them all. Now, I'm not g
72	oing to make you them all. Now, I'm not going to make you them all. Now, I'm not going to make you sit through every single one, but I do sit through every single one, but I do sit through every singl
73	e one, but I do want you to see. We'll do the first one. want you to see. We'll do the first one. want you to see. We'll do the first one. Got to make sure you turn the sound on. Got to make sure you 
74	turn the sound on. Got to make sure you turn the sound on. Hit play. Hey guys, welcome back. I am Hit play. Hey guys, welcome back. I am Hit play. Hey guys, welcome back. I am ostous. I'm going to do 
75	lowercase for my ostous. I'm going to do lowercase for my ostous. I'm going to do lowercase for my trigger word. just gonna be ostrichous. trigger word. just gonna be ostrichous. trigger word. just go
76	nna be ostrichous. I find with these models, uh, like the I find with these models, uh, like the I find with these models, uh, like the modern models, since they're used to modern models, since they'r
77	e used to modern models, since they're used to like natural language, they're used to like natural language, they're used to like natural language, they're used to names. So, if you do like trigger wo
78	rds, names. So, if you do like trigger words, names. So, if you do like trigger words, it doesn't seem to work as well as it doesn't seem to work as well as it doesn't seem to work as well as actually
79	 like if I were to write my full actually like if I were to write my full actually like if I were to write my full name here or whatever. I can do ostress name here or whatever. I can do ostress name 
80	here or whatever. I can do ostress because it doesn't really know what that because it doesn't really know what that because it doesn't really know what that is. So, it can just associate that with is
81	. So, it can just associate that with is. So, it can just associate that with me. Okay. So, I just have ostress says, "Hey Okay. So, I just have ostress says, "Hey guys, welcome back. I am ostress." N
82	ice, guys, welcome back. I am ostress." Nice, guys, welcome back. I am ostress." Nice, simple, easy. We're going to do that to simple, easy. We're going to do that to simple, easy. We're going to do t
83	hat to all these. Um, I'm just going to speed all these. Um, I'm just going to speed all these. Um, I'm just going to speed through all this real quick. I do want through all this real quick. I do wan
84	t through all this real quick. I do want to do things a little different when I to do things a little different when I to do things a little different when I have something like when I point at have s
85	omething like when I point at have something like when I point at myself or something, I'll caption for myself or something, I'll caption for myself or something, I'll caption for that. Right now, we'
86	re just putting that. Right now, we're just putting that. Right now, we're just putting ostra says and we have it in quotes. Um, ostra says and we have it in quotes. Um, ostra says and we have it in q
87	uotes. Um, depending on what you're doing, if depending on what you're doing, if depending on what you're doing, if you're doing different scenes, like I you're doing different scenes, like I you're d
88	oing different scenes, like I want to burn in this scene. If you want to burn in this scene. If you want to burn in this scene. If you don't, then you can put webcam scene, don't, then you can put web
89	cam scene, don't, then you can put webcam scene, you know, white walls, plants in the you know, white walls, plants in the you know, white walls, plants in the background, mirror in the background. ba
90	ckground, mirror in the background. background, mirror in the background. you if you don't want the clothes to get you if you don't want the clothes to get you if you don't want the clothes to get bur
91	ned in, then you can describe the burned in, then you can describe the burned in, then you can describe the clothes. It's still going to burn them clothes. It's still going to burn them clothes. It's 
92	still going to burn them in a little bit because it hasn't seen in a little bit because it hasn't seen in a little bit because it hasn't seen anything else. That'll make the anything else. That'll mak
93	e the anything else. That'll make the reference to ostress not include those reference to ostress not include those reference to ostress not include those concepts or at least weekly include concepts 
94	or at least weekly include concepts or at least weekly include those concepts. I want everything to those concepts. I want everything to those concepts. I want everything to look exactly like this. I'
95	m just going look exactly like this. I'm just going look exactly like this. I'm just going to burn that in. So, let's go through to burn that in. So, let's go through to burn that in. So, let's go thr
96	ough and I'll caption everything. and I'll caption everything. and I'll caption everything. All right. I wanted to clarify on this All right. I wanted to clarify on this All right. I wanted to clarify
97	 on this one. Uh, so most of these I just say one. Uh, so most of these I just say one. Uh, so most of these I just say Austra says Austra says. I don't mention Austra says Austra says. I don't mentio
98	n Austra says Austra says. I don't mention my hand movements because that's a part my hand movements because that's a part my hand movements because that's a part of my character. On this one though, 
99	of my character. On this one though, of my character. On this one though, I'll show you. However, I have rights to I'll show you. However, I have rights to I'll show you. However, I have rights to the
100	 IP of one character, the IP of one character, the IP of one character, this guy. So, I have it. However, I have this guy. So, I have it. However, I have this guy. So, I have it. However, I have right
101	s to the IP of one character and rights to the IP of one character and rights to the IP of one character and then I have he points at his face with then I have he points at his face with then I have h
102	e points at his face with both hands and says, so I want to be both hands and says, so I want to be both hands and says, so I want to be able to prompt in certain gestures so able to prompt in certain
103	 gestures so able to prompt in certain gestures so I'm not always just sitting there I'm not always just sitting there I'm not always just sitting there pointing at my face. Although I'm kind pointing
104	 at my face. Although I'm kind pointing at my face. Although I'm kind of pointing at my face in a lot of these of pointing at my face in a lot of these of pointing at my face in a lot of these videos 
105	cuz it's it's a great pointing videos cuz it's it's a great pointing videos cuz it's it's a great pointing face. This should allow us to give a face. This should allow us to give a face. This should a
106	llow us to give a little more control. And if you want little more control. And if you want little more control. And if you want complete control, every hand movement, complete control, every hand mov
107	ement, complete control, every hand movement, every everything, you can caption for every everything, you can caption for every everything, you can caption for that. The more you caption, the more tha
108	t. The more you caption, the more that. The more you caption, the more it'll learn those movements and that it'll learn those movements and that it'll learn those movements and that those movements ar
109	e associated with those movements are associated with those movements are associated with those words. Uh if you just want it to those words. Uh if you just want it to those words. Uh if you just want
110	 it to where you just say so and so says like where you just say so and so says like where you just say so and so says like I'm doing here, then we'll keep them I'm doing here, then we'll keep them I'
111	m doing here, then we'll keep them where we mostly just have the words that where we mostly just have the words that where we mostly just have the words that are being said. It's captioned. So, I did 
112	notice a few It's captioned. So, I did notice a few things I wanted to talk about. You can things I wanted to talk about. You can things I wanted to talk about. You can notice on this video, notice on
113	 this video, notice on this video, my face and my scruffy facial hair, my face and my scruffy facial hair, my face and my scruffy facial hair, everything about this whole essence is everything about t
114	his whole essence is everything about this whole essence is going to be burned into the Laura. I going to be burned into the Laura. I going to be burned into the Laura. I wanted to make sure I put wav
115	ing his wanted to make sure I put waving his wanted to make sure I put waving his hands around um because I don't want hands around um because I don't want hands around um because I don't want when I'
116	m just talking about anything when I'm just talking about anything when I'm just talking about anything that my hands are constantly waving that my hands are constantly waving that my hands are consta
117	ntly waving around my face. Although I wave my hands around my face. Although I wave my hands around my face. Although I wave my hands around a lot in this video. Another around a lot in this video. A
118	nother around a lot in this video. Another thing is there's a few times like the thing is there's a few times like the thing is there's a few times like the way that people talk is not the way they wa
119	y that people talk is not the way they way that people talk is not the way they write. Like for instance, I would write write. Like for instance, I would write write. Like for instance, I would write 
120	we're going to, but I actually say going we're going to, but I actually say going we're going to, but I actually say going to. I don't know if that's an accent or to. I don't know if that's an accent 
121	or to. I don't know if that's an accent or whatever, but that's what I say. We're whatever, but that's what I say. We're whatever, but that's what I say. We're going to do whatever. We're going to do 
122	going to do whatever. We're going to do going to do whatever. We're going to do whatever. So, I'm actually going to whatever. So, I'm actually going to whatever. So, I'm actually going to write Ghana 
123	here. So, that way it write Ghana here. So, that way it write Ghana here. So, that way it actually matches my voice and it doesn't actually matches my voice and it doesn't actually matches my voice an
124	d it doesn't confuse the model and that I will confuse the model and that I will confuse the model and that I will actually say everything that is typed. actually say everything that is typed. actuall
125	y say everything that is typed. So, if I say gonna, it's gonna write So, if I say gonna, it's gonna write So, if I say gonna, it's gonna write gonna. And if I say going to, it's going gonna. And if I 
126	say going to, it's going gonna. And if I say going to, it's going to write going to. That's how we want it to write going to. That's how we want it to write going to. That's how we want it to be. So, 
127	don't correct the way you to be. So, don't correct the way you to be. So, don't correct the way you speak or the way the person speaks. speak or the way the person speaks. speak or the way the person 
128	speaks. Okay, here I misspeak. Okay, here I misspeak. Okay, here I misspeak. Let me just show you Let me just show you Let me just show you >> because we want to be able to chop it up >> because we wa
129	nt to be able to chop it up >> because we want to be able to chop it up where I'm being very introspective and where I'm being very introspective and where I'm being very introspective and we I want t
130	o be excited and we I want to we I want to be excited and we I want to we I want to be excited and we I want to and we I want to be and we I want to and and we I want to be and we I want to and and we
131	 I want to be and we I want to and we I want to be and we I so I want to we I want to be and we I so I want to we I want to be and we I so I want to make sure I put that I don't want it make sure I pu
132	t that I don't want it make sure I put that I don't want it just randomly throwing in slurs in my just randomly throwing in slurs in my just randomly throwing in slurs in my voice because I want this 
133	like I can voice because I want this like I can voice because I want this like I can make better content than I actually can make better content than I actually can make better content than I actually
134	 can by not having the edible what in my by not having the edible what in my by not having the edible what in my voice. Okay, so we're going to get rid voice. Okay, so we're going to get rid voice. Ok
135	ay, so we're going to get rid of that. Um, but the way to get rid of of that. Um, but the way to get rid of of that. Um, but the way to get rid of it is we have to caption that I did the it is we have
136	 to caption that I did the it is we have to caption that I did the and what wait part. So, we did all that. and what wait part. So, we did all that. and what wait part. So, we did all that. That's how
137	 we caption it. It's pretty That's how we caption it. It's pretty That's how we caption it. It's pretty simple. Unless I'm doing something out simple. Unless I'm doing something out simple. Unless I'm
138	 doing something out of the ordinary here. Um, I'm mostly of the ordinary here. Um, I'm mostly of the ordinary here. Um, I'm mostly just saying Austra says that's what he just saying Austra says that'
139	s what he just saying Austra says that's what he says. Uh, if I'm starting kind of says. Uh, if I'm starting kind of says. Uh, if I'm starting kind of midsinut, so I chopped it up during a midsinut, s
140	o I chopped it up during a midsinut, so I chopped it up during a break where it doesn't start on a and break where it doesn't start on a and break where it doesn't start on a and another thing like on
141	 this one. another thing like on this one. another thing like on this one. And unfortunately, it's I'm continuing a And unfortunately, it's I'm continuing a And unfortunately, it's I'm continuing a se
142	ntence, so I'm not capitalizing it sentence, so I'm not capitalizing it sentence, so I'm not capitalizing it here. But I do capitalize it if it's the here. But I do capitalize it if it's the here. But
143	 I do capitalize it if it's the start of my paragraph. So maybe the start of my paragraph. So maybe the start of my paragraph. So maybe the model will pick up on that, maybe it model will pick up on t
144	hat, maybe it model will pick up on that, maybe it won't. I don't know. Let's just get won't. I don't know. Let's just get won't. I don't know. Let's just get started. But before we do, let's take a s
145	tarted. But before we do, let's take a started. But before we do, let's take a look at the actual lengths of these look at the actual lengths of these look at the actual lengths of these videos. So I 
146	have some that are 5 videos. So I have some that are 5 videos. So I have some that are 5 seconds, some are four, some are seven, seconds, some are four, some are seven, seconds, some are four, some ar
147	e seven, six, four, five. I try to do all around six, four, five. I try to do all around six, four, five. I try to do all around five. Some of these are a little longer. five. Some of these are a litt
148	le longer. five. Some of these are a little longer. Um, if you're on a tight GPU, you Um, if you're on a tight GPU, you Um, if you're on a tight GPU, you probably want to go short. In fact, you probab
149	ly want to go short. In fact, you probably want to go short. In fact, you may want to do really short sentences, may want to do really short sentences, may want to do really short sentences, uh, for t
150	raining at least. Um, I'm going uh, for training at least. Um, I'm going uh, for training at least. Um, I'm going up to like eight, a little over eight. I up to like eight, a little over eight. I up t
```

> AGENT

The transcript is triplicated (each line appears 3x). Let me deduplicate and read the rest.

> TOOL

tool_use Bash
```json
{
  "command": "cat /tmp/ostris-ltx/ostris.en.srt | grep -v \"^[0-9]*$\" | grep -v \"^[0-9]*:[0-9]*\" | grep -v \"^$\" | awk '!seen[$0]++' > /tmp/ostris-ltx/dedup.txt && wc -l /tmp/ostris-ltx/dedup.txt && wc -w /tmp/ostris-ltx/dedup.txt",
  "description": "Dedupe SRT lines"
}
```

> TOOL

tool_result Bash
```
1545 /tmp/ostris-ltx/dedup.txt
   11200 /tmp/ostris-ltx/dedup.txt
```

> AGENT

Not relevant to this read-and-summarize task. Continuing.

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/dedup.txt",
  "offset": 1,
  "limit": 400
}
```

> TOOL

tool_result Read
```
1	Hey guys, welcome back. I am Ostress.
2	Hey guys, welcome back. I am Ostress.
3	 
4	Today we are going to train an LTX 2.3
5	Today we are going to train an LTX 2.3
6	character Laura. So, you're probably
7	character Laura. So, you're probably
8	noticing something a little different
9	noticing something a little different
10	here. Most of my videos, we zoom in on a
11	here. Most of my videos, we zoom in on a
12	blank screen on my monitor in front of
13	blank screen on my monitor in front of
14	me, and I am just an ethereal voice
15	me, and I am just an ethereal voice
16	talking in the background. But today, we
17	talking in the background. But today, we
18	need some content. We need something to
19	need some content. We need something to
20	train on. We need a character to train
21	train on. We need a character to train
22	on. And unfortunately, it's really hard
23	on. And unfortunately, it's really hard
24	to get rights to the IP of a character.
25	to get rights to the IP of a character.
26	However, I have rights to the IP of one
27	However, I have rights to the IP of one
28	character,
29	character,
30	this guy. So, I'm going to start out
31	this guy. So, I'm going to start out
32	with this video. This video is going to
33	with this video. This video is going to
34	be the exact video I use to train the
35	be the exact video I use to train the
36	character Laura. We're going to go
37	character Laura. We're going to go
38	through, we're going to cut out scenes
39	through, we're going to cut out scenes
40	from this video, cut out my little
41	from this video, cut out my little
42	pieces of text that I do, and we are
43	pieces of text that I do, and we are
44	going to train an LTX 2.3 Laura on this.
45	going to train an LTX 2.3 Laura on this.
46	So, we should be able to generate all of
47	So, we should be able to generate all of
48	this with our Laura. I'm going to burn
49	this with our Laura. I'm going to burn
50	in the background. I'm going to burn in
51	in the background. I'm going to burn in
52	my clothes. I'm going to burn in my face
53	my clothes. I'm going to burn in my face
54	and my scruffy facial hair. Everything
55	and my scruffy facial hair. Everything
56	about this whole essence is going to be
57	about this whole essence is going to be
58	burned into the Laura. So then I, you,
59	burned into the Laura. So then I, you,
60	whoever can just sit here and generate
61	whoever can just sit here and generate
62	your own ostress content. To get
63	your own ostress content. To get
64	started, I have to make a lot of
65	started, I have to make a lot of
66	expressions. I have to talk kind of slow
67	expressions. I have to talk kind of slow
68	at points because we want to be able to
69	at points because we want to be able to
70	chop it up where I'm being very
71	chop it up where I'm being very
72	introspective and we I want to be
73	introspective and we I want to be
74	excited on some things. LTX 2.3 is going
75	excited on some things. LTX 2.3 is going
76	to learn the voice. It's going to learn
77	to learn the voice. It's going to learn
78	how I talk. It's going to learn the
79	how I talk. It's going to learn the
80	inflections of my voice. It's going to
81	inflections of my voice. It's going to
82	learn the clothing I wear. It's going to
83	learn the clothing I wear. It's going to
84	learn everything about me. If we can
85	learn everything about me. If we can
86	chop all of this up properly. Let's just
87	chop all of this up properly. Let's just
88	get started. I'm going to take all this.
89	get started. I'm going to take all this.
90	We're going to pack it down. Let's hop
91	We're going to pack it down. Let's hop
92	over into KDEN Live. It's open source
93	over into KDEN Live. It's open source
94	software. And from there, we're going to
95	software. And from there, we're going to
96	chop this up into little pieces. and
97	chop this up into little pieces. and
98	we're going to build our data set so
99	we're going to build our data set so
100	that we can train our own ostress
101	that we can train our own ostress
102	character Laura. Okay, I have KD and
103	character Laura. Okay, I have KD and
104	live pulled up. I'll put a link of this
105	live pulled up. I'll put a link of this
106	in the description
107	in the description
108	that way you guys can see it. Let's just
109	that way you guys can see it. Let's just
110	drop in our clip here.
111	drop in our clip here.
112	Okay, it immediately asks, do we want to
113	Okay, it immediately asks, do we want to
114	switch? Yes, we do. This was recorded at
115	switch? Yes, we do. This was recorded at
116	1440.
117	1440.
118	All right, there wasn't audio. Let's
119	All right, there wasn't audio. Let's
120	drag that back in. Sometimes if you
121	drag that back in. Sometimes if you
122	don't see the audio track, there was no
123	don't see the audio track, there was no
124	audio. I'm not sure why that happened.
125	audio. I'm not sure why that happened.
126	So, we'll just kind of browse through
127	So, we'll just kind of browse through
128	here and see what we can come up with.
129	here and see what we can come up with.
130	The intro. Hey guys, welcome back. I am
131	The intro. Hey guys, welcome back. I am
132	ostrous. Today, we are going to train an
133	ostrous. Today, we are going to train an
134	LTX 2.3 character Laura. Perfect. So, I
135	LTX 2.3 character Laura. Perfect. So, I
136	just want to go through and trim this
137	just want to go through and trim this
138	up.
139	We want it where back. I am ostous. So,
140	We want it where back. I am ostous. So,
141	we can cut it out right here. So, that's
142	we can cut it out right here. So, that's
143	going to put us about 4 seconds. We want
144	going to put us about 4 seconds. We want
145	to do it where I'm not midway through a
146	to do it where I'm not midway through a
147	word. So, I have like a whole sentence
148	word. So, I have like a whole sentence
149	here or at least at a stopping point.
150	here or at least at a stopping point.
151	Hey guys, welcome back. I am ostrous.
152	Hey guys, welcome back. I am ostrous.
153	Boom. And we'll do it to there. So, all
154	Boom. And we'll do it to there. So, all
155	we got to do is drag this blue line to
156	we got to do is drag this blue line to
157	there. Then I come up here and I click
158	there. Then I come up here and I click
159	file and then we do render.
160	file and then we do render.
161	So, we're going to do it to
162	So, we're going to do it to
163	ostress_0000001.
164	Uh, right here, it's important. Select
165	Uh, right here, it's important. Select
166	selected zone. See, you can tell the
167	selected zone. See, you can tell the
168	time changes there when we go from full
169	time changes there when we go from full
170	project to selected zone. And that's
171	project to selected zone. And that's
172	just going to be our blue area here.
173	just going to be our blue area here.
174	So, then all of this is fine. Make sure
175	So, then all of this is fine. Make sure
176	we have audio
177	we have audio
178	render to file.
179	And that's our first clip. So, I'm just
180	And that's our first clip. So, I'm just
181	going to do that a bunch. I'll kind of
182	going to do that a bunch. I'll kind of
183	speed through that so you don't have to
184	speed through that so you don't have to
185	watch all the clips. And let's get our
186	watch all the clips. And let's get our
187	training data set.
188	So, we have 19 videos. I just chopped up
189	So, we have 19 videos. I just chopped up
190	everything you guys just watched. We
191	everything you guys just watched. We
192	broke it up into little pieces. Uh, the
193	broke it up into little pieces. Uh, the
194	pieces are in between, you know, two 3
195	pieces are in between, you know, two 3
196	seconds up to about 8, eight and a half,
197	seconds up to about 8, eight and a half,
198	I think, which all should be fine to
199	I think, which all should be fine to
200	train locally. So the next step, let's
201	train locally. So the next step, let's
202	go to AI toolkit. Let's get started.
203	go to AI toolkit. Let's get started.
204	Okay, I'm going to pop over to Runpod.
205	Okay, I'm going to pop over to Runpod.
206	I'm going to do this on RunPod. You can
207	I'm going to do this on RunPod. You can
208	train this locally. You can train this
209	train this locally. You can train this
210	on a 5090 at home doing full layer
211	on a 5090 at home doing full layer
212	offloading. I'll show you guys how to do
213	offloading. I'll show you guys how to do
214	that. Uh but just for speed and
215	that. Uh but just for speed and
216	everything. I'm going to do Runpod. I'll
217	everything. I'm going to do Runpod. I'll
218	post a link in the description of how to
219	post a link in the description of how to
220	set all this up. I have a whole video on
221	set all this up. I have a whole video on
222	how to use RunOD. And if you're going to
223	how to use RunOD. And if you're going to
224	sign up for RunPod, use my affiliate
225	sign up for RunPod, use my affiliate
226	link. That kind of helps me out so that
227	link. That kind of helps me out so that
228	I can train videos like this. uh gives
229	I can train videos like this. uh gives
230	me some credits for this. So, I'm going
231	me some credits for this. So, I'm going
232	to use an RTX Pro.
233	So, let's go over here. First thing I
234	So, let's go over here. First thing I
235	have to do is I have to build the data
236	have to do is I have to build the data
237	set on our brand new pod. New data set.
238	set on our brand new pod. New data set.
239	We're just going to name this Austri.
240	We're just going to name this Austri.
241	So, now I'm just going to drag and drop
242	So, now I'm just going to drag and drop
243	these videos over. Oh, and you guys get
244	these videos over. Oh, and you guys get
245	to see the new drag and drop uploader.
246	to see the new drag and drop uploader.
247	Works significantly better doing one
248	Works significantly better doing one
249	video at a time.
250	video at a time.
251	Much better.
252	Much better.
253	I know that needed improvement. A lot of
254	I know that needed improvement. A lot of
255	people complained. That should solve the
256	people complained. That should solve the
257	issues. Let me know if you still have
258	issues. Let me know if you still have
259	problems. So, now what we got to do here
260	problems. So, now what we got to do here
261	is go through the videos and caption
262	is go through the videos and caption
263	them all. Now, I'm not going to make you
264	them all. Now, I'm not going to make you
265	sit through every single one, but I do
266	sit through every single one, but I do
267	want you to see. We'll do the first one.
268	want you to see. We'll do the first one.
269	Got to make sure you turn the sound on.
270	Got to make sure you turn the sound on.
271	Hit play. Hey guys, welcome back. I am
272	Hit play. Hey guys, welcome back. I am
273	ostous. I'm going to do lowercase for my
274	ostous. I'm going to do lowercase for my
275	trigger word. just gonna be ostrichous.
276	trigger word. just gonna be ostrichous.
277	I find with these models, uh, like the
278	I find with these models, uh, like the
279	modern models, since they're used to
280	modern models, since they're used to
281	like natural language, they're used to
282	like natural language, they're used to
283	names. So, if you do like trigger words,
284	names. So, if you do like trigger words,
285	it doesn't seem to work as well as
286	it doesn't seem to work as well as
287	actually like if I were to write my full
288	actually like if I were to write my full
289	name here or whatever. I can do ostress
290	name here or whatever. I can do ostress
291	because it doesn't really know what that
292	because it doesn't really know what that
293	is. So, it can just associate that with
294	is. So, it can just associate that with
295	me.
296	Okay. So, I just have ostress says, "Hey
297	Okay. So, I just have ostress says, "Hey
298	guys, welcome back. I am ostress." Nice,
299	guys, welcome back. I am ostress." Nice,
300	simple, easy. We're going to do that to
301	simple, easy. We're going to do that to
302	all these. Um, I'm just going to speed
303	all these. Um, I'm just going to speed
304	through all this real quick. I do want
305	through all this real quick. I do want
306	to do things a little different when I
307	to do things a little different when I
308	have something like when I point at
309	have something like when I point at
310	myself or something, I'll caption for
311	myself or something, I'll caption for
312	that. Right now, we're just putting
313	that. Right now, we're just putting
314	ostra says and we have it in quotes. Um,
315	ostra says and we have it in quotes. Um,
316	depending on what you're doing, if
317	depending on what you're doing, if
318	you're doing different scenes, like I
319	you're doing different scenes, like I
320	want to burn in this scene. If you
321	want to burn in this scene. If you
322	don't, then you can put webcam scene,
323	don't, then you can put webcam scene,
324	you know, white walls, plants in the
325	you know, white walls, plants in the
326	background, mirror in the background.
327	background, mirror in the background.
328	you if you don't want the clothes to get
329	you if you don't want the clothes to get
330	burned in, then you can describe the
331	burned in, then you can describe the
332	clothes. It's still going to burn them
333	clothes. It's still going to burn them
334	in a little bit because it hasn't seen
335	in a little bit because it hasn't seen
336	anything else. That'll make the
337	anything else. That'll make the
338	reference to ostress not include those
339	reference to ostress not include those
340	concepts or at least weekly include
341	concepts or at least weekly include
342	those concepts. I want everything to
343	those concepts. I want everything to
344	look exactly like this. I'm just going
345	look exactly like this. I'm just going
346	to burn that in. So, let's go through
347	to burn that in. So, let's go through
348	and I'll caption everything.
349	and I'll caption everything.
350	All right. I wanted to clarify on this
351	All right. I wanted to clarify on this
352	one. Uh, so most of these I just say
353	one. Uh, so most of these I just say
354	Austra says Austra says. I don't mention
355	Austra says Austra says. I don't mention
356	my hand movements because that's a part
357	my hand movements because that's a part
358	of my character. On this one though,
359	of my character. On this one though,
360	I'll show you. However, I have rights to
361	I'll show you. However, I have rights to
362	the IP of one character,
363	the IP of one character,
364	this guy. So, I have it. However, I have
365	this guy. So, I have it. However, I have
366	rights to the IP of one character and
367	rights to the IP of one character and
368	then I have he points at his face with
369	then I have he points at his face with
370	both hands and says, so I want to be
371	both hands and says, so I want to be
372	able to prompt in certain gestures so
373	able to prompt in certain gestures so
374	I'm not always just sitting there
375	I'm not always just sitting there
376	pointing at my face. Although I'm kind
377	pointing at my face. Although I'm kind
378	of pointing at my face in a lot of these
379	of pointing at my face in a lot of these
380	videos cuz it's it's a great pointing
381	videos cuz it's it's a great pointing
382	face. This should allow us to give a
383	face. This should allow us to give a
384	little more control. And if you want
385	little more control. And if you want
386	complete control, every hand movement,
387	complete control, every hand movement,
388	every everything, you can caption for
389	every everything, you can caption for
390	that. The more you caption, the more
391	that. The more you caption, the more
392	it'll learn those movements and that
393	it'll learn those movements and that
394	those movements are associated with
395	those movements are associated with
396	those words. Uh if you just want it to
397	those words. Uh if you just want it to
398	where you just say so and so says like
399	where you just say so and so says like
400	I'm doing here, then we'll keep them
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/dedup.txt",
  "offset": 400,
  "limit": 450
}
```

> TOOL

tool_result Read
```
400	I'm doing here, then we'll keep them
401	I'm doing here, then we'll keep them
402	where we mostly just have the words that
403	where we mostly just have the words that
404	are being said.
405	It's captioned. So, I did notice a few
406	It's captioned. So, I did notice a few
407	things I wanted to talk about. You can
408	things I wanted to talk about. You can
409	notice on this video,
410	notice on this video,
411	my face and my scruffy facial hair,
412	my face and my scruffy facial hair,
413	everything about this whole essence is
414	everything about this whole essence is
415	going to be burned into the Laura. I
416	going to be burned into the Laura. I
417	wanted to make sure I put waving his
418	wanted to make sure I put waving his
419	hands around um because I don't want
420	hands around um because I don't want
421	when I'm just talking about anything
422	when I'm just talking about anything
423	that my hands are constantly waving
424	that my hands are constantly waving
425	around my face. Although I wave my hands
426	around my face. Although I wave my hands
427	around a lot in this video. Another
428	around a lot in this video. Another
429	thing is there's a few times like the
430	thing is there's a few times like the
431	way that people talk is not the way they
432	way that people talk is not the way they
433	write. Like for instance, I would write
434	write. Like for instance, I would write
435	we're going to, but I actually say going
436	we're going to, but I actually say going
437	to. I don't know if that's an accent or
438	to. I don't know if that's an accent or
439	whatever, but that's what I say. We're
440	whatever, but that's what I say. We're
441	going to do whatever. We're going to do
442	going to do whatever. We're going to do
443	whatever. So, I'm actually going to
444	whatever. So, I'm actually going to
445	write Ghana here. So, that way it
446	write Ghana here. So, that way it
447	actually matches my voice and it doesn't
448	actually matches my voice and it doesn't
449	confuse the model and that I will
450	confuse the model and that I will
451	actually say everything that is typed.
452	actually say everything that is typed.
453	So, if I say gonna, it's gonna write
454	So, if I say gonna, it's gonna write
455	gonna. And if I say going to, it's going
456	gonna. And if I say going to, it's going
457	to write going to. That's how we want it
458	to write going to. That's how we want it
459	to be. So, don't correct the way you
460	to be. So, don't correct the way you
461	speak or the way the person speaks.
462	speak or the way the person speaks.
463	Okay, here I misspeak.
464	Okay, here I misspeak.
465	Let me just show you
466	Let me just show you
467	>> because we want to be able to chop it up
468	>> because we want to be able to chop it up
469	where I'm being very introspective and
470	where I'm being very introspective and
471	we I want to be excited and we I want to
472	we I want to be excited and we I want to
473	and we I want to be and we I want to and
474	and we I want to be and we I want to and
475	we I want to be and we I so I want to
476	we I want to be and we I so I want to
477	make sure I put that I don't want it
478	make sure I put that I don't want it
479	just randomly throwing in slurs in my
480	just randomly throwing in slurs in my
481	voice because I want this like I can
482	voice because I want this like I can
483	make better content than I actually can
484	make better content than I actually can
485	by not having the edible what in my
486	by not having the edible what in my
487	voice. Okay, so we're going to get rid
488	voice. Okay, so we're going to get rid
489	of that. Um, but the way to get rid of
490	of that. Um, but the way to get rid of
491	it is we have to caption that I did the
492	it is we have to caption that I did the
493	and what wait part. So, we did all that.
494	and what wait part. So, we did all that.
495	That's how we caption it. It's pretty
496	That's how we caption it. It's pretty
497	simple. Unless I'm doing something out
498	simple. Unless I'm doing something out
499	of the ordinary here. Um, I'm mostly
500	of the ordinary here. Um, I'm mostly
501	just saying Austra says that's what he
502	just saying Austra says that's what he
503	says. Uh, if I'm starting kind of
504	says. Uh, if I'm starting kind of
505	midsinut, so I chopped it up during a
506	midsinut, so I chopped it up during a
507	break where it doesn't start on a and
508	break where it doesn't start on a and
509	another thing like on this one.
510	another thing like on this one.
511	And unfortunately, it's I'm continuing a
512	And unfortunately, it's I'm continuing a
513	sentence, so I'm not capitalizing it
514	sentence, so I'm not capitalizing it
515	here. But I do capitalize it if it's the
516	here. But I do capitalize it if it's the
517	start of my paragraph. So maybe the
518	start of my paragraph. So maybe the
519	model will pick up on that, maybe it
520	model will pick up on that, maybe it
521	won't. I don't know. Let's just get
522	won't. I don't know. Let's just get
523	started. But before we do, let's take a
524	started. But before we do, let's take a
525	look at the actual lengths of these
526	look at the actual lengths of these
527	videos. So I have some that are 5
528	videos. So I have some that are 5
529	seconds, some are four, some are seven,
530	seconds, some are four, some are seven,
531	six, four, five. I try to do all around
532	six, four, five. I try to do all around
533	five. Some of these are a little longer.
534	five. Some of these are a little longer.
535	Um, if you're on a tight GPU, you
536	Um, if you're on a tight GPU, you
537	probably want to go short. In fact, you
538	probably want to go short. In fact, you
539	may want to do really short sentences,
540	may want to do really short sentences,
541	uh, for training at least. Um, I'm going
542	uh, for training at least. Um, I'm going
543	up to like eight, a little over eight. I
544	up to like eight, a little over eight. I
545	think I have like four videos here that
546	think I have like four videos here that
547	are over eight, some four. So, for the
548	are over eight, some four. So, for the
549	most part, I'm trying to keep it around
550	most part, I'm trying to keep it around
551	five. Um, but you can always chop it
552	five. Um, but you can always chop it
553	that way. That's good. Perfect. Let's go
554	that way. That's good. Perfect. Let's go
555	to new job. ostress webcam LTX 2.3
556	to new job. ostress webcam LTX 2.3
557	which we got to do that. Getting a lot
558	which we got to do that. Getting a lot
559	of models in here. Let's go down. LTX
560	of models in here. Let's go down. LTX
561	2.3. Perfect. I'm going to leave all
562	2.3. Perfect. I'm going to leave all
563	this on float 8 for now. Uh just cuz I'm
564	this on float 8 for now. Uh just cuz I'm
565	on a big nice GPU. Um if you're doing
566	on a big nice GPU. Um if you're doing
567	this locally, like let's say you're on I
568	this locally, like let's say you're on I
569	think you can do this on a 5090. You
570	think you can do this on a 5090. You
571	should be able to use most of these
572	should be able to use most of these
573	settings on a 5090. If you're going to
574	settings on a 5090. If you're going to
575	do that, just do layer offloading. just
576	do that, just do layer offloading. just
577	offload everything. Um, we're going to
578	offload everything. Um, we're going to
579	cache everything later, but yeah, you
580	cache everything later, but yeah, you
581	probably just want to offload the full
582	probably just want to offload the full
583	thing to train this locally, but I'm
584	thing to train this locally, but I'm
585	going to leave it on float.
586	going to leave it on float.
587	Linear rank 32. That should be plenty.
588	Linear rank 32. That should be plenty.
589	On the steps, I have it at 30,000 here.
590	On the steps, I have it at 30,000 here.
591	These videos, remember, we're not just
592	These videos, remember, we're not just
593	learning images here. This is more than
594	learning images here. This is more than
595	just this is what this person looks
596	just this is what this person looks
597	like. It's this what this person looks
598	like. It's this what this person looks
599	like as they're moving their mouth, as
600	like as they're moving their mouth, as
601	they're talking, as their hands are
602	they're talking, as their hands are
603	waving. What do their hands look like?
604	waving. What do their hands look like?
605	What does the room look like? How does
606	What does the room look like? How does
607	their voice sound? What kind of
608	their voice sound? What kind of
609	inflections is this? It's so much more
610	inflections is this? It's so much more
611	than just a picture. I mean, you can
612	than just a picture. I mean, you can
613	train a character in just 3,000 steps
614	train a character in just 3,000 steps
615	for a picture. For doing actual video
616	for a picture. For doing actual video
617	like this, it's going to take more. Now,
618	like this, it's going to take more. Now,
619	I only have one scene here, so it may
620	I only have one scene here, so it may
621	not take as much. We'll see. But yeah,
622	not take as much. We'll see. But yeah,
623	I'm going to go ahead and bump this up.
624	I'm going to go ahead and bump this up.
625	I'm going to do it to 10.
626	I'm going to do it to 10.
627	Um, it may not take that, it may take
628	Um, it may not take that, it may take
629	that. We'll just find out. The rest of
630	that. We'll just find out. The rest of
631	this, I can leave all this mostly the
632	this, I can leave all this mostly the
633	same. Depending on what kind of video
634	same. Depending on what kind of video
635	you're doing, if you're doing all kinds
636	you're doing, if you're doing all kinds
637	of this character, doing all these
638	of this character, doing all these
639	different scenes, and you want the model
640	different scenes, and you want the model
641	to be just as functional it is as it is
642	to be just as functional it is as it is
643	now, I would actually leave all this
644	now, I would actually leave all this
645	alone. But since I'm trying to overwrite
646	alone. But since I'm trying to overwrite
647	the whole scene, and LTX has a pretty
648	the whole scene, and LTX has a pretty
649	heavy shift when it generates, so it
650	heavy shift when it generates, so it
651	does a lot of those high noise time
652	does a lot of those high noise time
653	steps when it's generating. I'm going to
654	steps when it's generating. I'm going to
655	set this on high noise. If you want it
656	set this on high noise. If you want it
657	to train faster, set it on high noise.
658	to train faster, set it on high noise.
659	Uh, you can always switch this to
660	Uh, you can always switch this to
661	balanced at the end. Um, that's probably
662	balanced at the end. Um, that's probably
663	a pretty good bet for most things, I
664	a pretty good bet for most things, I
665	would say. We want to make sure that
666	would say. We want to make sure that
667	we're going to cache the text
668	we're going to cache the text
669	embeddings. We wrote all the captions,
670	embeddings. We wrote all the captions,
671	so we don't unload. Unload's just for
672	so we don't unload. Unload's just for
673	trigger words. We want to cache the text
674	trigger words. We want to cache the text
675	embeddings. You can read about that
676	embeddings. You can read about that
677	here. That way, we can get rid of that
678	here. That way, we can get rid of that
679	text encoder completely. We don't want
680	text encoder completely. We don't want
681	to keep it around. Also, keep low VRAM
682	to keep it around. Also, keep low VRAM
683	on here. Even if you're on a RTX 6000,
684	on here. Even if you're on a RTX 6000,
685	you know, I have 96 gigs of VRAMm on a
686	you know, I have 96 gigs of VRAMm on a
687	video model, everything's low VRAM. A
688	video model, everything's low VRAM. A
689	lot of this is the Vay. When it's
690	lot of this is the Vay. When it's
691	decoding the Vay, uh, decoding the video
692	decoding the Vay, uh, decoding the video
693	into the pixel space and the video
694	into the pixel space and the video
695	space, it's a very VRAMm intensive
696	space, it's a very VRAMm intensive
697	process. So, with low VRAMm, it'll
698	process. So, with low VRAMm, it'll
699	actually split it up into smaller clips,
700	actually split it up into smaller clips,
701	and it'll decode them little by little
702	and it'll decode them little by little
703	and patch it all together. Uh, it
704	and patch it all together. Uh, it
705	doesn't affect quality much, but it does
706	doesn't affect quality much, but it does
707	save a ton of VRAMm. It's not that much
708	save a ton of VRAMm. It's not that much
709	slower. It's just during generation.
710	slower. It's just during generation.
711	Anyway, leave it on. It doesn't slow
712	Anyway, leave it on. It doesn't slow
713	down training at all. Our data set is
714	down training at all. Our data set is
715	ostress. That's the only one I have.
716	ostress. That's the only one I have.
717	Hopefully, you're using this a lot. And
718	Hopefully, you're using this a lot. And
719	you have a ton of them here. That'd be
720	you have a ton of them here. That'd be
721	awesome.
722	awesome.
723	Going to leave most of this the same.
724	Going to leave most of this the same.
725	Make sure cache latences on. It's on by
726	Make sure cache latences on. It's on by
727	default for the 2.3 model. Cache the
728	default for the 2.3 model. Cache the
729	latence. Cash the video because it
730	latence. Cash the video because it
731	doesn't just encode them. It has to
732	doesn't just encode them. It has to
733	split up the video. It has to shrink the
734	split up the video. It has to shrink the
735	video to match our frame rate. There's a
736	video to match our frame rate. There's a
737	lot of stuff that goes on to make the
738	lot of stuff that goes on to make the
739	latence. Just cache them. It does them
740	latence. Just cache them. It does them
741	once. Saves it to disk and you're done.
742	once. Saves it to disk and you're done.
743	The other big thing, in fact, I'll
744	The other big thing, in fact, I'll
745	probably have this set as default going
746	probably have this set as default going
747	forward. Now that I think about it,
748	forward. Now that I think about it,
749	autoframe count. So, normally you'd have
750	autoframe count. So, normally you'd have
751	to figure out, okay, it's 24 frames a
752	to figure out, okay, it's 24 frames a
753	second. How many seconds are we? We
754	second. How many seconds are we? We
755	divide that out and you figure out how
756	divide that out and you figure out how
757	many frames you have plus one. You can
758	many frames you have plus one. You can
759	read about it here.
760	read about it here.
761	Or that button does it all. It's going
762	Or that button does it all. It's going
763	to It doesn't matter if it's four
764	to It doesn't matter if it's four
765	seconds, doesn't matter if it's five
766	seconds, doesn't matter if it's five
767	seconds. They can be different lengths.
768	seconds. They can be different lengths.
769	You aren't going to get that chip monkey
770	You aren't going to get that chip monkey
771	voice. Doesn't have to be exact. It's
772	voice. Doesn't have to be exact. It's
773	gonna automatically figure it out. For
774	gonna automatically figure it out. For
775	me, it's the best quality of life thing
776	me, it's the best quality of life thing
777	I've done in a while. Now, if you are
778	I've done in a while. Now, if you are
779	training locally, like on a 5090, you
780	training locally, like on a 5090, you
781	may, especially if you're 8second clips,
782	may, especially if you're 8second clips,
783	you may want to stick with 51.2. It's
784	you may want to stick with 51.2. It's
785	going to learn really good at 51.2. Um,
786	going to learn really good at 51.2. Um,
787	on mine, I have a 1080p webcam, but
788	on mine, I have a 1080p webcam, but
789	honestly, it doesn't get the 1080p. Um,
790	honestly, it doesn't get the 1080p. Um,
791	I'm just going to do 512 and 768. I can
792	I'm just going to do 512 and 768. I can
793	always add the higher resolutions later
794	always add the higher resolutions later
795	after it kind of learns it. But starting
796	after it kind of learns it. But starting
797	out, I'm just going to do 512 768. These
798	out, I'm just going to do 512 768. These
799	are if it's a square. It's not a square,
800	are if it's a square. It's not a square,
801	but it's the same amount of pixels as a
802	but it's the same amount of pixels as a
803	square. So, it's not quite 720. This is
804	square. So, it's not quite 720. This is
805	probably closer to 720p. All right. Now,
806	probably closer to 720p. All right. Now,
807	we have samples for LTX 2.3. The frame
808	we have samples for LTX 2.3. The frame
809	rate is burned in or it's set at 24
810	rate is burned in or it's set at 24
811	frames a second. So, you can multiply
812	frames a second. So, you can multiply
813	that. you have to add an additional
814	that. you have to add an additional
815	frame. So 5 seconds * 24 + 1 you get 121
816	frame. So 5 seconds * 24 + 1 you get 121
817	basically. So that's 5 seconds of video.
818	basically. So that's 5 seconds of video.
819	You can increase this but the formula is
820	You can increase this but the formula is
821	take the amount of seconds* 24 add one.
822	take the amount of seconds* 24 add one.
823	You can make it whatever length you
824	You can make it whatever length you
825	want. But keep in mind this is still
826	want. But keep in mind this is still
827	process intensive even though it's not
828	process intensive even though it's not
829	training. Not to mention it takes
830	training. Not to mention it takes
831	forever. If you're going to do 10 videos
832	forever. If you're going to do 10 videos
833	that's ridiculous. I mean this you'll
834	that's ridiculous. I mean this you'll
835	spend way more time generating videos
836	spend way more time generating videos
837	than you will training. We don't need
838	than you will training. We don't need
839	that many. All right. Before we get into
840	that many. All right. Before we get into
841	all the samples, I want to go over
842	all the samples, I want to go over
843	height here. So, this normally does a
844	height here. So, this normally does a
845	square, but all of my videos are in 169
846	square, but all of my videos are in 169
847	format or widescreen format. So, I'm not
848	format or widescreen format. So, I'm not
849	generating at actual 1080p or 720p
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/dedup.txt",
  "offset": 850,
  "limit": 400
}
```

> TOOL

tool_result Read
```
850	generating at actual 1080p or 720p
851	resolution. I'm not training at that
852	resolution. I'm not training at that
853	either. All of these are set up for like
854	either. All of these are set up for like
855	512 x 512. And so, you want to match the
856	512 x 512. And so, you want to match the
857	same amount of pixels roughly. I want to
858	same amount of pixels roughly. I want to
859	do it at 768. But basically, we just
860	do it at 768. But basically, we just
861	make this square. So, it'll be the same
862	make this square. So, it'll be the same
863	amount of pixels roughly as 768 x 768.
864	amount of pixels roughly as 768 x 768.
865	Instead, we'll do 1024
866	by 576.
867	by 576.
868	And that'll be a 16-9 aspect ratio, but
869	And that'll be a 16-9 aspect ratio, but
870	while maintaining 768
871	while maintaining 768
872	dimensions.
873	dimensions.
874	Um, so that you're not blowing up the
875	Um, so that you're not blowing up the
876	model. Uh if you need to save VRAM even
877	model. Uh if you need to save VRAM even
878	more, you can go smaller. So you can do
879	more, you can go smaller. So you can do
880	680 by 384. That'll be equivalent to 512
881	680 by 384. That'll be equivalent to 512
882	x 512. So if you're just training on 512
883	x 512. So if you're just training on 512
884	and you just want to sample real quick,
885	and you just want to sample real quick,
886	680x 384. If you want to do 768 x 768,
887	680x 384. If you want to do 768 x 768,
888	the equivalent is 1024 x 576. And
889	the equivalent is 1024 x 576. And
890	that'll just make it where we're at a
891	that'll just make it where we're at a
892	with five.
893	with five.
894	Ostress says, "I think the real question
895	Ostress says, "I think the real question
896	is, is this going to work?"
897	is, is this going to work?"
898	Austria says, "I trained this Laura on
899	Austria says, "I trained this Laura on
900	Ostrous AI toolkit."
901	Ostrous AI toolkit."
902	So, those are just I'm just saying
903	So, those are just I'm just saying
904	stuff. I will also want to test can we
905	stuff. I will also want to test can we
906	add other things to the model it didn't
907	add other things to the model it didn't
908	train on. So, I have here ostress holds
909	train on. So, I have here ostress holds
910	up an orange tabby cat. He kisses it and
911	up an orange tabby cat. He kisses it and
912	says, "This little fluffball is my cat,
913	says, "This little fluffball is my cat,
914	Zapod." Ostress says, "And then everyone
915	Zapod." Ostress says, "And then everyone
916	started acting crazy." He leans forward
917	started acting crazy." He leans forward
918	to the camera and says, "Which was good
919	to the camera and says, "Which was good
920	because I like crazy." Ostress is
921	because I like crazy." Ostress is
922	dancing to rave music and he says, "If
923	dancing to rave music and he says, "If
924	you turn this up loud enough, you can
925	you turn this up loud enough, you can
926	really feel your eardrums bursting."
927	really feel your eardrums bursting."
928	Let's see if it can do any of this. We
929	Let's see if it can do any of this. We
930	don't have music. We don't have a cat.
931	don't have music. We don't have a cat.
932	Um, we're doing movements. I don't know
933	Um, we're doing movements. I don't know
934	if it's going to work. We'll see what
935	if it's going to work. We'll see what
936	happens. That is enough talking. Let's
937	happens. That is enough talking. Let's
938	create the job.
939	create the job.
940	Then from here, we just give it a start.
941	Then from here, we just give it a start.
942	While I'm here, you may notice there's a
943	While I'm here, you may notice there's a
944	new um little button here. Uh this was
945	new um little button here. Uh this was
946	highly requested. I don't like light
947	highly requested. I don't like light
948	mode, but I guess a lot of people do.
949	mode, but I guess a lot of people do.
950	So,
951	So,
952	you can click that if you want light
953	you can click that if you want light
954	mode. It'll remember it.
955	mode. It'll remember it.
956	You can see it's caching the latence to
957	You can see it's caching the latence to
958	the disc. I mean, it's got to do this
959	the disc. I mean, it's got to do this
960	for every size that we're training on.
961	for every size that we're training on.
962	And look at this. At the smaller one,
963	And look at this. At the smaller one,
964	it's 9 seconds for a single video
965	it's 9 seconds for a single video
966	because it's got to chop up the video.
967	because it's got to chop up the video.
968	It's got to reshrink. It's got to shrink
969	It's got to reshrink. It's got to shrink
970	it. It's got to remap it. So, always
971	it. It's got to remap it. So, always
972	cash latent with the video models. Just
973	cash latent with the video models. Just
974	do it. Otherwise, it'd be doing this
975	do it. Otherwise, it'd be doing this
976	every training step. 9 seconds extra to
977	every training step. 9 seconds extra to
978	the training step. So, just cash latent.
979	the training step. So, just cash latent.
980	Do it. Do it. I'm not going to keep
981	Do it. Do it. I'm not going to keep
982	saying it. Do it. First samples done. We
983	saying it. Do it. First samples done. We
984	are at step 29. It's going 8.16 seconds
985	are at step 29. It's going 8.16 seconds
986	in iteration, averaging 7.7 seconds in
987	in iteration, averaging 7.7 seconds in
988	iteration. We're at 54.7 GB of VRAM.
989	iteration. We're at 54.7 GB of VRAM.
990	Again, you have to offload to get this
991	Again, you have to offload to get this
992	to work if you're on consumer grade
993	to work if you're on consumer grade
994	hardware, but I have 95.6 GB, so I'm not
995	hardware, but I have 95.6 GB, so I'm not
996	doing that. Let's go check out the
997	doing that. Let's go check out the
998	samples.
999	samples.
1000	>> I think the real question is, is this
1001	>> I think the real question is, is this
1002	going to work?
1003	going to work?
1004	>> Clearly not me. Let's do the next.
1005	>> Clearly not me. Let's do the next.
1006	>> Says, "I trained this Laura on Ostris AI
1007	>> Says, "I trained this Laura on Ostris AI
1008	toolkit."
1009	toolkit."
1010	>> Okay.
1011	>> Okay.
1012	>> This little fluffball is my cat, Zafod.
1013	>> This little fluffball is my cat, Zafod.
1014	>> Kind of close to the right, man.
1015	>> Kind of close to the right, man.
1016	>> This little fluffball is my cat. Zafod
1017	>> This little fluffball is my cat. Zafod
1018	>> says, "And then everyone started acting
1019	>> says, "And then everyone started acting
1020	crazy, which was good cuz I like crazy."
1021	crazy, which was good cuz I like crazy."
1022	>> If you turn this up loud enough, you can
1023	>> If you turn this up loud enough, you can
1024	really feel your eardrums bursting.
1025	really feel your eardrums bursting.
1026	>> Okay, so none of these are me.
1027	>> Okay, so none of these are me.
1028	Obviously, a lot of them actually say
1029	Obviously, a lot of them actually say
1030	ostress said
1031	ostress said
1032	>> says I trained this
1033	>> says I trained this
1034	>> you know interesting. Okay, so that
1035	>> you know interesting. Okay, so that
1036	should all go away. Hopefully goes away
1037	should all go away. Hopefully goes away
1038	pretty fast. We'll see what happens
1039	pretty fast. We'll see what happens
1040	next. Revisit. Revisit. This is probably
1041	next. Revisit. Revisit. This is probably
1042	not your first time here. You know the
1043	not your first time here. You know the
1044	drill. Let's skip on ahead. The first
1045	drill. Let's skip on ahead. The first
1046	samples are in. Let's see if we're
1047	samples are in. Let's see if we're
1048	making progress. Okay. Yeah. I mean,
1049	making progress. Okay. Yeah. I mean,
1050	it's definitely more like me than these.
1051	it's definitely more like me than these.
1052	Let's take a listen. I think the real
1053	Let's take a listen. I think the real
1054	question is, is this going to work? Wow,
1055	question is, is this going to work? Wow,
1056	that's getting my voice down very quick.
1057	that's getting my voice down very quick.
1058	I trained this Laura on Ostus AI
1059	I trained this Laura on Ostus AI
1060	toolkit. I Oh man, it's working so fast.
1061	toolkit. I Oh man, it's working so fast.
1062	I'm super impressed. This little
1063	I'm super impressed. This little
1064	fluffball is my cat, Zafod.
1065	fluffball is my cat, Zafod.
1066	>> It's getting Zod wrong, but I mean the
1067	>> It's getting Zod wrong, but I mean the
1068	voice is it's nailing the voice. And
1069	voice is it's nailing the voice. And
1070	then everyone started acting crazy,
1071	then everyone started acting crazy,
1072	which was good because I like crazy. And
1073	which was good because I like crazy. And
1074	and it's, you know, it can tell like
1075	and it's, you know, it can tell like
1076	this is like a webcam. He has the chair.
1077	this is like a webcam. He has the chair.
1078	I mean, it's definitely getting it. I
1079	I mean, it's definitely getting it. I
1080	mean, from back here, you know, they
1081	mean, from back here, you know, they
1082	were all over the place. Now,
1083	were all over the place. Now,
1084	you know, it's
1085	you know, it's
1086	>> Oh man, I can't wait to see this. I
1087	>> Oh man, I can't wait to see this. I
1088	always train on other things and other
1089	always train on other things and other
1090	people. It's going to be kind of weird
1091	people. It's going to be kind of weird
1092	to see me cuz I know my face better than
1093	to see me cuz I know my face better than
1094	anyone. I'll notice like freckles are in
1095	anyone. I'll notice like freckles are in
1096	the wrong spot and things like that.
1097	the wrong spot and things like that.
1098	Let's see where this goes. I'm super
1099	Let's see where this goes. I'm super
1100	pumped up. Okay, it's been a few hours.
1101	pumped up. Okay, it's been a few hours.
1102	We are at step 20,000 now. We have a lot
1103	We are at step 20,000 now. We have a lot
1104	of samples. Let's go take a look. Okay,
1105	of samples. Let's go take a look. Okay,
1106	so we're just going to go down so we can
1107	so we're just going to go down so we can
1108	see the progression. Um, I won't play
1109	see the progression. Um, I won't play
1110	all the audio and everything until we
1111	all the audio and everything until we
1112	get down towards the bottom. So, we just
1113	get down towards the bottom. So, we just
1114	go
1115	go
1116	Nice. Nice.
1117	Nice. Nice.
1118	Oh, yeah. It's picking it up. My little
1119	Oh, yeah. It's picking it up. My little
1120	nerdy glasses and beanie and everything.
1121	nerdy glasses and beanie and everything.
1122	All right, down here. We're looking
1123	All right, down here. We're looking
1124	pretty good. Let's listen to them.
1125	pretty good. Let's listen to them.
1126	I think the real question is, is this
1127	I think the real question is, is this
1128	>> I trained this Laura on Ostus AI
1129	>> I trained this Laura on Ostus AI
1130	toolkit. Hitskisserris. This little
1131	toolkit. Hitskisserris. This little
1132	fluff ball is my cat, Zafod.
1133	fluff ball is my cat, Zafod.
1134	Hitskisserris. Let's get the name wrong.
1135	Hitskisserris. Let's get the name wrong.
1136	>> And then everyone started acting crazy,
1137	>> And then everyone started acting crazy,
1138	which was good because I like crazy. If
1139	which was good because I like crazy. If
1140	There's a few things here I want to take
1141	There's a few things here I want to take
1142	note of. We're at step 2000. This is
1143	note of. We're at step 2000. This is
1144	actually looking pretty good.
1145	actually looking pretty good.
1146	>> And then see back here, this is like
1147	>> And then see back here, this is like
1148	really choppy. Doesn't look like it's
1149	really choppy. Doesn't look like it's
1150	great quality.
1151	great quality.
1152	>> It's I think
1153	>> It's I think
1154	>> it's different every scene. But for the
1155	>> it's different every scene. But for the
1156	most part, my scenes
1157	most part, my scenes
1158	>> I trained.
1159	>> I trained.
1160	>> Oh my gosh, that's annoying. For the
1161	>> Oh my gosh, that's annoying. For the
1162	most part, my scenes are looking, you
1163	most part, my scenes are looking, you
1164	know, consistent across each one, and
1165	know, consistent across each one, and
1166	that's because we're doing the high
1167	that's because we're doing the high
1168	noise time steps. Uh, but I do want to
1169	noise time steps. Uh, but I do want to
1170	stop it.
1171	stop it.
1172	Now, you could keep going with this if
1173	Now, you could keep going with this if
1174	you wanted to, and you'd be good. Uh,
1175	you wanted to, and you'd be good. Uh,
1176	I'm about to go to sleep, so we're going
1177	I'm about to go to sleep, so we're going
1178	to let it train overnight, and we'll see
1179	to let it train overnight, and we'll see
1180	where it goes. So, I want to change a
1181	where it goes. So, I want to change a
1182	few things here. I actually don't think
1183	few things here. I actually don't think
1184	we we're not going to need that many.
1185	we we're not going to need that many.
1186	I'll have it stop halfway through the
1187	I'll have it stop halfway through the
1188	night. So, we'll we'll go to 5,000. That
1189	night. So, we'll we'll go to 5,000. That
1190	should be good. I'm going to change this
1191	should be good. I'm going to change this
1192	from high noise to balanced. So before
1193	from high noise to balanced. So before
1194	it was it really focus on the higher
1195	it was it really focus on the higher
1196	noise time steps. And when you're
1197	noise time steps. And when you're
1198	sampling generally you kind of focus on
1199	sampling generally you kind of focus on
1200	those a lot more uh with the shift. But
1201	those a lot more uh with the shift. But
1202	this is just going to allow us to you
1203	this is just going to allow us to you
1204	know clean up that finer detail towards
1205	know clean up that finer detail towards
1206	the end. So I'm going to set it on that
1207	the end. So I'm going to set it on that
1208	to clean up the fine detail. So that's
1209	to clean up the fine detail. So that's
1210	where it's good to do balance. You
1211	where it's good to do balance. You
1212	probably don't want to go to low noise
1213	probably don't want to go to low noise
1214	because it'll break down your high noise
1215	because it'll break down your high noise
1216	um everything you already trained. So,
1217	um everything you already trained. So,
1218	we'll just leave it on balanced. One
1219	we'll just leave it on balanced. One
1220	more thing I'm going to do. You don't
1221	more thing I'm going to do. You don't
1222	have to do this. Uh, but I have a big
1223	have to do this. Uh, but I have a big
1224	GPU, so I'm going to do it. I'm going to
1225	GPU, so I'm going to do it. I'm going to
1226	turn on 1024. I have plenty of RAM here,
1227	turn on 1024. I have plenty of RAM here,
1228	so I'm going to go up to this. Uh, you
1229	so I'm going to go up to this. Uh, you
1230	can get by with these lower ones.
1231	can get by with these lower ones.
1232	Generally, it's fine. Other than that,
1233	Generally, it's fine. Other than that,
1234	I'm going to leave everything else the
1235	I'm going to leave everything else the
1236	same. I'm going to start it, update the
1237	same. I'm going to start it, update the
1238	job,
1239	job,
1240	hit play, and I'm going to go brush my
1241	hit play, and I'm going to go brush my
1242	teeth, go to bed, and tomorrow morning,
1243	teeth, go to bed, and tomorrow morning,
1244	we'll see what we got. And we're done.
1245	we'll see what we got. And we're done.
1246	5,000 steps. Let's go take a look. Let's
1247	5,000 steps. Let's go take a look. Let's
1248	see what we got.
1249	see what we got.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/tmp/ostris-ltx/dedup.txt",
  "offset": 1249,
  "limit": 300
}
```

> TOOL

tool_result Read
```
1249	see what we got.
1250	Okay, that is me.
1251	Okay, that is me.
1252	That looks just like the videos.
1253	That looks just like the videos.
1254	Perfect. Let's give a listen. I think
1255	Perfect. Let's give a listen. I think
1256	the real question is, is this going to
1257	the real question is, is this going to
1258	work? I trained this Laura on Ostus AI
1259	work? I trained this Laura on Ostus AI
1260	toolkit.
1261	toolkit.
1262	>> That's a
1263	>> That's a
1264	>> I trained this little fluffball is my
1265	>> I trained this little fluffball is my
1266	cat Zafod. And then everyone started
1267	cat Zafod. And then everyone started
1268	acting crazy,
1269	acting crazy,
1270	>> which was good because I like crazy. If
1271	>> which was good because I like crazy. If
1272	really feel your eardrums bursting. I'm
1273	really feel your eardrums bursting. I'm
1274	I'm very happy with that. there's some
1275	I'm very happy with that. there's some
1276	of the super fine detail it's not
1277	of the super fine detail it's not
1278	picking up. But I think we can fix that
1279	picking up. But I think we can fix that
1280	uh using different samplers, raising
1281	uh using different samplers, raising
1282	CFG. We can kind of play around with
1283	CFG. We can kind of play around with
1284	that a little bit. Plus, when we go to
1285	that a little bit. Plus, when we go to
1286	the turbo model, cuz I find it works
1287	the turbo model, cuz I find it works
1288	really good if you train on the base
1289	really good if you train on the base
1290	model and then actually use the turbo
1291	model and then actually use the turbo
1292	model to generate. I find that that
1293	model to generate. I find that that
1294	works a lot better. Let's quit talking.
1295	works a lot better. Let's quit talking.
1296	I'm going to download this.
1297	I'm going to download this.
1298	Come over here. You can download the
1299	Come over here. You can download the
1300	latest one here. Uh, I'm going to load
1301	latest one here. Uh, I'm going to load
1302	this up in the Comfy and let's give it
1303	this up in the Comfy and let's give it
1304	uh let's give it a shot. Okay, so we got
1305	uh let's give it a shot. Okay, so we got
1306	everything loaded up in the Comfy UI.
1307	everything loaded up in the Comfy UI.
1308	I'm going to start with the distilled
1309	I'm going to start with the distilled
1310	version. Um, I don't think we actually
1311	version. Um, I don't think we actually
1312	need the dev version. In fact, I I kind
1313	need the dev version. In fact, I I kind
1314	of like the results of the distilled
1315	of like the results of the distilled
1316	version better most of the time. Austra
1317	version better most of the time. Austra
1318	says, I'm going to try to run this.
1319	says, I'm going to try to run this.
1320	Okay, I can't read that. It's too small.
1321	Okay, I can't read that. It's too small.
1322	Austra says, so I'm going to try to run
1323	Austra says, so I'm going to try to run
1324	this in Comfy UI first. I want to see
1325	this in Comfy UI first. I want to see
1326	how good it does with the distilled
1327	how good it does with the distilled
1328	version.
1329	So, I am going to try to run this in
1330	So, I am going to try to run this in
1331	Comfy UI. First, I want to see how good
1332	Comfy UI. First, I want to see how good
1333	it does with the distilled version. I
1334	it does with the distilled version. I
1335	think it does pretty good. Okay. Okay.
1336	think it does pretty good. Okay. Okay.
1337	So, now let's have some fun. Uh, it's
1338	So, now let's have some fun. Uh, it's
1339	clearly it's working. Um, I need longer
1340	clearly it's working. Um, I need longer
1341	text. A few things. First, we have the
1342	text. A few things. First, we have the
1343	length here. I'm going to go and make
1344	length here. I'm going to go and make
1345	this a different color. So, 121. This is
1346	this a different color. So, 121. This is
1347	5 seconds. So if you do 24 frames a
1348	5 seconds. So if you do 24 frames a
1349	second, which I have set up here, 24
1350	second, which I have set up here, 24
1351	frames a second time 5 is 120 plus you
1352	frames a second time 5 is 120 plus you
1353	add the one key frame. So I want to do
1354	add the one key frame. So I want to do
1355	significantly longer text.
1356	significantly longer text.
1357	So let's see what we can do because one
1358	So let's see what we can do because one
1359	thing is you see how I'm talking fast.
1360	thing is you see how I'm talking fast.
1361	Try to run this in comfy UI. First I
1362	Try to run this in comfy UI. First I
1363	want to see how good it does with the
1364	want to see how good it does with the
1365	distilled version. Everything we trained
1366	distilled version. Everything we trained
1367	on actually fits inside of a sentence
1368	on actually fits inside of a sentence
1369	structure or you know it fills the whole
1370	structure or you know it fills the whole
1371	video. There's no dead air at different
1372	video. There's no dead air at different
1373	points. So, we kind of taught it to as
1374	points. So, we kind of taught it to as
1375	soon as the video starts, I start
1376	soon as the video starts, I start
1377	talking and I talk however fast or
1378	talking and I talk however fast or
1379	however slow to fill the time. Let's do
1380	however slow to fill the time. Let's do
1381	it out to 10 seconds just to see how it
1382	it out to 10 seconds just to see how it
1383	responds differently. So, we do 10 * 24
1384	responds differently. So, we do 10 * 24
1385	and you add one. I guess I don't need a
1386	and you add one. I guess I don't need a
1387	calculator to add one, but we're going
1388	calculator to add one, but we're going
1389	to do it anyway. So, 241 is going to get
1390	to do it anyway. So, 241 is going to get
1391	us 10 seconds.
1392	So, I'm guessing it's going to slow down
1393	So, I'm guessing it's going to slow down
1394	our audio quite a bit. So, I am going to
1395	our audio quite a bit. So, I am going to
1396	try to run this in Comfy UI first. I
1397	try to run this in Comfy UI first. I
1398	distilled version. All right, that's
1399	distilled version. All right, that's
1400	pretty good. Um, let's try to do it at
1401	pretty good. Um, let's try to do it at
1402	higher quality. Okay, so I'm going to do
1403	higher quality. Okay, so I'm going to do
1404	this at
1405	1280 by 720. So, this is 720p,
1406	1280 by 720. So, this is 720p,
1407	the original high definition. We'll
1408	the original high definition. We'll
1409	switch that back to 121. Give us one
1410	switch that back to 121. Give us one
1411	second because we're doing higher
1412	second because we're doing higher
1413	resolution here. So, let's see if a lot
1414	resolution here. So, let's see if a lot
1415	of these artifacts clean up and stuff
1416	of these artifacts clean up and stuff
1417	like that. Ostress holds up the largest
1418	like that. Ostress holds up the largest
1419	hamburger in the world and says, "I'm
1420	hamburger in the world and says, "I'm
1421	going to try to eat this entire
1422	going to try to eat this entire
1423	hamburger in one bite." He quickly eats
1424	hamburger in one bite." He quickly eats
1425	the hamburger one bite. I don't know if
1426	the hamburger one bite. I don't know if
1427	it's going to be able to do this, but
1428	it's going to be able to do this, but
1429	let's give it a run.
1430	All right, the quality looks a little
1431	All right, the quality looks a little
1432	better. Let's see what we have. I am
1433	better. Let's see what we have. I am
1434	hamburger in one bite.
1435	hamburger in one bite.
1436	>> Well, he doesn't eat it. And that's
1437	>> Well, he doesn't eat it. And that's
1438	definitely not the largest hamburger in
1439	definitely not the largest hamburger in
1440	the world. Let's try to go up to 1080p.
1441	the world. Let's try to go up to 1080p.
1442	So that's significantly larger
1443	So that's significantly larger
1444	resolution, especially than what we
1445	resolution, especially than what we
1446	trained on. All right,
1447	trained on. All right,
1448	let's give that a run. It should go kind
1449	let's give that a run. It should go kind
1450	of slow, but it should be able to handle
1451	of slow, but it should be able to handle
1452	it.
1453	it.
1454	It generated 1080p. Let's see what we
1455	It generated 1080p. Let's see what we
1456	have. I am going to try to eat this
1457	have. I am going to try to eat this
1458	entire hamburger in one bite. The
1459	entire hamburger in one bite. The
1460	quality looks really good. I'm super
1461	quality looks really good. I'm super
1462	impressed with that. Him holding the
1463	impressed with that. Him holding the
1464	hamburger or I guess me holding the
1465	hamburger or I guess me holding the
1466	hamburger is a little off. So, let's try
1467	hamburger is a little off. So, let's try
1468	some other stuff here. All right, we'll
1469	some other stuff here. All right, we'll
1470	just do something simple. Austria says,
1471	just do something simple. Austria says,
1472	"Training Allora super easy with AI
1473	"Training Allora super easy with AI
1474	toolkit." Let's try it.
1475	toolkit." Let's try it.
1476	Training Allora is super easy with AI
1477	Training Allora is super easy with AI
1478	toolkit. Training Allora.
1479	toolkit. Training Allora.
1480	Okay. Absolutely. I like I I'm blown
1481	Okay. Absolutely. I like I I'm blown
1482	away with how good it looks. It looks so
1483	away with how good it looks. It looks so
1484	much like me. I spend all of this time
1485	much like me. I spend all of this time
1486	making this content, like making all
1487	making this content, like making all
1488	these videos. And I want to do more
1489	these videos. And I want to do more
1490	videos, and I'm kind of wondering if
1491	videos, and I'm kind of wondering if
1492	it'd be easier for me to just write some
1493	it'd be easier for me to just write some
1494	scripts and have this dude do it instead
1495	scripts and have this dude do it instead
1496	of me. Um, that would be significantly
1497	of me. Um, that would be significantly
1498	easier. Let's end the video that way.
1499	easier. Let's end the video that way.
1500	Well, guys, that is it for me. That is
1501	Well, guys, that is it for me. That is
1502	how you can train your own LTX 2.3
1503	how you can train your own LTX 2.3
1504	character Laura with Ostus AI toolkit.
1505	character Laura with Ostus AI toolkit.
1506	We trained on a single person in a
1507	We trained on a single person in a
1508	single scene which allows us to generate
1509	single scene which allows us to generate
1510	not only a consistent character but a
1511	not only a consistent character but a
1512	consistent scene and consistent clothing
1513	consistent scene and consistent clothing
1514	as well. I will post links in the
1515	as well. I will post links in the
1516	description to the workflow that I use
1517	description to the workflow that I use
1518	to generate these 10-second 1080p videos
1519	to generate these 10-second 1080p videos
1520	on a 5090 in under 4 minutes. And if you
1521	on a 5090 in under 4 minutes. And if you
1522	like my work or you use my work in a
1523	like my work or you use my work in a
1524	professional setting, please consider
1525	professional setting, please consider
1526	becoming a supporter. Just head over to
1527	becoming a supporter. Just head over to
1528	oustress.comsupport.
1529	oustress.comsupport.
1530	There you can see numerous ways to
1531	There you can see numerous ways to
1532	support me by donating or buying merch.
1533	support me by donating or buying merch.
1534	Plus, you can see the people and
1535	Plus, you can see the people and
1536	organizations that already selflessly
1537	organizations that already selflessly
1538	donated to help make all of this
1539	donated to help make all of this
1540	possible. That's it. I'm AI generated
1541	possible. That's it. I'm AI generated
1542	and I will see you next time. Or the
1543	and I will see you next time. Or the
1544	real ostress will. But I'm out. Bye.
1545	Huh?
1546
```

> AGENT

I have all the information. Let me write the report.

# LTX 2.3 Character LoRA — Ostris Tutorial Notes

## 1. Dataset
- **19 clips**, mostly ~5s, range 2–8.5s. "We have 19 videos... the pieces are in between, you know, two 3 seconds up to about 8, eight and a half." Try to target ~5s; "I try to do all around five."
- Source recorded at **1440p** webcam, 16:9. "This was recorded at 1440." "I have a 1080p webcam, but honestly, it doesn't get the 1080p."
- Cut in **Kdenlive** (open source); render selected zone with audio.
- Cut at natural sentence boundaries: "We want to do it where I'm not midway through a word."
- **Manual captions**, no auto-caption. Format: `ostress says, "<the spoken words>"`. Lowercase trigger, prefer real name over synthetic token: "since they're used to natural language... if you do like trigger words, it doesn't seem to work as well." Caption verbatim — don't normalize "gonna" to "going to": "don't correct the way you speak."
- Caption deviations only (point-at-face, hand waves, mid-sentence chops): "he points at his face with both hands and says." Capitalize at paragraph start, not mid-sentence continuations.
- Single scene to **burn in** scene/clothes/background; do NOT describe what you want burned in.

## 2. Model / base
- **LTX 2.3** (base, not turbo/distilled). Selected from AI Toolkit's model dropdown. "I find it works really good if you train on the base model and then actually use the turbo model to generate."

## 3. Training config
- **Quantization**: float8 ("I'm going to leave all this on float 8 for now").
- **LoRA**: Linear, **rank 32**. "Linear rank 32. That should be plenty." (No alpha mentioned.)
- **Steps**: started at 30,000, sampled every 2,000, **stopped at 5,000** ("we'll go to 5,000. That should be good"). At 3,000 was already "looking pretty good"; at 2,000 "actually looking pretty good."
- **Timestep schedule**: start on **high noise** then switch to **balanced** for fine detail. "LTX has a pretty heavy shift... set this on high noise. If you want it to train faster, set it on high noise... switch this to balanced at the end... don't want to go to low noise because it'll break down your high noise."
- **Cache text embeddings**: ON (deletes text encoder). "We want to cache the text embeddings... get rid of that text encoder completely."
- **Cache latents**: ON, default for 2.3. "9 seconds extra to the training step. So, just cache latent. Do it."
- **Auto frame count**: ON. Internally 24 fps, `frames = seconds*24 + 1`.
- **Training resolutions (buckets)**: started **512 and 768**, added **1024** for the second/overnight run. "I can always add the higher resolutions later." Note: he calls 51.2 in a passage about local 5090 8s clips — likely 512.
- Optimizer, LR, scheduler, batch size, grad accumulation: **not covered** (left at AI Toolkit defaults — "leave most of this the same").

## 4. Hardware / runtime
- **RunPod RTX Pro** (RTX 6000 Pro / 96 GB) for the demo. "I'm going to use an RTX Pro... I have 96 gigs of VRAM."
- **VRAM used**: 54.7 GB at step 29. "We're at 54.7 GB of VRAM... I have 95.6 GB."
- **Speed**: ~7.7–8.16 s/it. "Going 8.16 seconds in iteration, averaging 7.7 seconds."
- **Local alt**: 5090 with **full layer offloading**, prefer shorter clips at 51.2 (likely 512). "You can train this on a 5090 at home doing full layer offloading."
- **Low VRAM toggle**: ON always for video models (chunked VAE decode). "Even if you're on a RTX 6000... on a video model, everything's low VRAM."

## 5. Sampling during training
- Sample resolution: he changed default square to **1024×576** (16:9 at ~768 equivalent). For 512 equivalent use **680×384**. "Maintaining 768 dimensions."
- Sample length 121 frames = 5s. Few prompts only: "ostress says I think the real question..."; "ostress holds up an orange tabby cat... Zapod"; rave-music dancing; "trained this Laura on Ostris AI Toolkit." Mix of in-distribution + out-of-distribution (cat, music, dancing) to probe generalization.
- Watch for: voice mimicry (came in fast), face/freckles, scene consistency, and "ostress" leaking into captions as text in output (expected to fade).
- "You'll spend way more time generating videos than you will training. We don't need that many."

## 6. Inference
- **ComfyUI**, **LTX 2.3 distilled** (turbo) at inference even though trained on base. "I kind of like the results of the distilled version better most of the time."
- 24 fps, frames = seconds*24+1 (121 for 5s, 241 for 10s).
- Resolutions tested: 720p (1280×720), then **1080p**.
- "10-second 1080p videos on a 5090 in under 4 minutes."
- LoRA weight: not stated. Levers for fine detail: "different samplers, raising CFG."

## 7. Tips / gotchas
- **Caption verbatim speech**, including disfluencies and slurs, so you can later prompt them out — "we have to caption that I did the 'and what wait' part" to remove stutters at inference.
- **Burn-in vs. describe**: anything you describe in captions is dissociated from trigger; anything you omit gets burned into the character. Don't describe clothes/background if you want them locked.
- **High noise first, balanced later** — never finish on low-noise-focused schedule, "it'll break down your high noise."
- **Always cache latents** for video models; otherwise +9 s/step.
- **Don't oversize sample resolution** during training — "you're not blowing up the model."
- Video LoRA needs more steps than image (~3k for image, more for video) but he stopped at 5k.
- Auto-frame-count handles mixed-length clips without "chipmunk voice."
- 8s clips on a 5090 → stick to 51.2 (likely 512) and short sentences.
- Local-only: use full layer offloading.
