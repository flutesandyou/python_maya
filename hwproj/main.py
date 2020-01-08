from maya import cmds

def run():
	# get objects
	objs = cmds.ls(sl=1, l=1)

	# get playback settings
	startTime = int(cmds.playbackOptions(q=1, min=1))
	endTime = int(cmds.playbackOptions(q=1, max=1))
	timeRange = range(startTime, endTime + 1)
	allDict = {}
	attrDict = {}
	for o in objs:
		print ("object", o)
		attrs = cmds.listAnimatable(o)
		frames = cmds.keyframe(obj, q=True, at=attr)
        values = cmds.keyframe(obj, q=True, at=attr, vc=True)            
		for t in timeRange:
			print ("frame", t)
			for a in attrs:
				print a
				val = cmds.keyframe(o, at=a, t=(t,t) ,ev=1, q=1)
				if val == None:
					val = cmds.getAttr(a, t=t)
				#print val
				attrDict[a] = val
			allDict[t] = attrDict
	print allDict
