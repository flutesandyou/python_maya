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
    attrs = cmds.listAttr(objs, keyable=True)
    frames = []
    values = []
    for o in objs:
        for a in attrs:
            if cmds.keyframe(objs, q=True, at=a):
                frames.append(cmds.keyframe(objs, q=True, at=a))
            if cmds.keyframe(objs, q=True, at=a, vc=True):
                values.append(cmds.keyframe(objs, q=True, at=a, vc=True))
        print frames
        print values

