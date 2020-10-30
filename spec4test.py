from floor_plans.spec import BuildingSpec

spec = BuildingSpec(population=500)
preks = [
    spec.add_room('PK', 1041),
    spec.add_room('PK', 1050),
    spec.add_room('PK', 1079),
]
ks = [
    spec.add_room('K', 1090),
    spec.add_room('K', 1105),
    spec.add_room('K', 1093),
    spec.add_room('K', 1110),
    spec.add_room('K', 1105),
]
firsts = [
    spec.add_room('1', 872),
    spec.add_room('1', 882),
    spec.add_room('1', 877),
    spec.add_room('1', 879),
    spec.add_room('1', 883),
]
seconds = [
    spec.add_room('2', 872),
    spec.add_room('2', 882),
    spec.add_room('2', 877),
    spec.add_room('2', 879),
    spec.add_room('2', 883),
]

spec.add_room('team', 328)
spec.add_room('work', 503)
spec.add_room('janitorial', 181)
spec.add_room('title 1', 526)
spec.add_room('tutoring', 106+222+113+111+112)
spec.add_room('conference', 251)
spec.add_room('resource', 872)

spec.add_room('none1', 1104)
spec.add_room('autism', 835)
spec.add_room('proj', 942)
spec.add_room('music', area=900)
spec.add_room('art', area=1076)
spec.add_room('life skills', area=825)

spec.add_room('storage1', area=227)
spec.add_room('OT/PT', area=503)
spec.add_room('faculty', area=482)

gym = spec.add_room('gym', area=6993)
stage = spec.add_room('stage', area=915)
cafeteria = spec.add_room('cafeteria', area=3811)

kitchen = spec.add_room('kitchen', area=1701)
spec.add_room('boiler', area=1316)
spec.add_room('library', area=2637)
spec.add_room('administration', area=3303)
spec.add_room('administration', area=3281)

spec.add_room('none2', area=659)
spec.add_room('electrical', area=365)
spec.add_room('computer lab', area=636)

spec.add_room('bldg storage', area=731)
spec.add_room('recycle', area=229)
spec.add_room('custodial', area=330)

spec.add_room('playground', area=10000, outside=True)


spec.add_variable_room('toilet', 200)
for i in range(1):
    spec.add_room('toilet', area=200)

spec.add_variable_room('empty', 800)
for i in range(3):
    spec.add_room('empty', area=800)

spec.add_requirement(gym, stage, 'adjacent')
spec.add_requirement(cafeteria, kitchen, 'adjacent')

