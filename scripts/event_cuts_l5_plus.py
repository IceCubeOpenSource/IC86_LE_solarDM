from math import cos
def event_cuts(frame):
	if not(frame.Has("IC86_Dunkman_L6_PegLeg_MultiNest8D_Track")):
		return False
	if not(frame.Has("IC86_Dunkman_L6_PegLeg_MultiNest8D_HDCasc")):
		return False
	if not(frame.Has("IC86_Dunkman_L6_PegLeg_MultiNest8D_NumuCC")):
		return False
	if frame.Has("IC86_Dunkman_L1") and not frame["IC86_Dunkman_L1"].value:
		return False
	if frame.Has("IC86_Dunkman_L2") and not frame["IC86_Dunkman_L2"].value:
		return False
	if frame.Has("IC86_Dunkman_L3") and not frame["IC86_Dunkman_L3"].value:
		return False
	if frame.Has("IC2011_LE_L3_NORT") and not frame["IC2011_LE_L3_NORT"].value:
		return False
	if frame.Has("IC86_Dunkman_L6_SANTA_DirectDOMs") and frame["IC86_Dunkman_L6_SANTA_DirectDOMs"].value < 3:
		return False
	if frame.Has("IC86_Dunkman_L4") and frame["IC86_Dunkman_L4"]["result"] != 1:
		return False
	if frame.Has("IC86_Dunkman_L5") and frame["IC86_Dunkman_L5"]["bdt_score"] <= 0.1:
		return False
	if frame["IC86_Dunkman_L6"]["mn_start_contained"] == 0:
		return False
	if frame["IC86_Dunkman_L6_CorridorDOMs"].value > 1:
		return False
