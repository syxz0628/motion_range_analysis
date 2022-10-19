# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 15:27:59 2022

@author: ysheng
"""
import argparse
import anamotion_range

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--patientID", required=False, help="IDcd . of the patient")
    parser.add_argument("-p","--planname", required=False, help="name of the specific plan")
    parser.add_argument("-lp", "--logpath", required=False, help="path of the log file?(exp: ./1.log,./2.log,./3.log)")
    parser.add_argument("-ld", "--logdim", required=False, help="the log file is 3D or 4D?(exp: 3D,4D,4D)")
    parser.add_argument("-m","--motionlist", required=False, help="Target/OAR name list to be analysised for motion")
    parser.add_argument("-r", "--rangefield", required=True, help="analysis range for which field name?")
    parser.add_argument("-s", "--statelist", required=False, help="which state to analysis motion and/or range <for range ana, state 0 is forced to analysis>")
    parser.add_argument("-sn","--savename", required=False, help="additional save to file name")
    parser.add_argument("-sp", "--save2path", required=False, help="path of save to file")
    #parser.add_argument("-t", "--timeoffset", required=False, type=int, nargs='+',
    #                    help="Time offset in msec,to adjust results in ~250ms level that was added to system determined timeoffset value;multiple values are acceptable, e.g. -t 250 -250 100",
    #                    default=250)
    #parser.add_argument("-g", "--log", required=False, nargs='?',
    #                    help="write error/successed information to .log file")
    args = parser.parse_args()

# define mandatory parameters.
    patientID=args.patientID
    planname=args.planname
    try:
        motionlist = args.motionlist.split(',')
        loglist=args.logpath.split(',')
        logdimlist = args.logdim.split(',')
        rangefield = args.rangefield.split(',')
        statelist = args.statelist.split(',')
    except:
        pass
    save2name=args.savename
    save2path=args.save2path

# call analysis_gd function
    analysis_mo_ra_data=anamotion_range.class_analysis_mo_ra(patientID,planname,loglist,logdimlist,statelist,save2path,save2name)
    if ( motionlist!=None):
        analysis_mo_ra_data.fun_analysis_motion(motionlist)
    if ( rangefield!=None):
        analysis_mo_ra_data.fun_analysis_range(rangefield)
