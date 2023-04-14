import relate_funs
import sys
class class_analysis_mo_ra:
    def __init__(self, patientID,planname,loglist,logdimlist,statelist,save2path1,save2path2,save2name):
        self.patientID=patientID
        self.planname=planname
        self.statelist=statelist
        self.savename=save2name
        self.save2rangepath=save2path1
        self.save2motionpath = save2path2
        self.loglist=loglist
        self.logdimlist=logdimlist # 4D / 3D?
        #
        # if patientID!=None and planname!=None:
        #     self.path2analog='/u/ysheng/MyAIXd/projects/patients/'+self.patientID+'/4DdoseRecon/exec/'+self.planname+'/'+self.planname+'_motion_range_ana.log'
        #     self.path2_3Danalog1 = '/u/ysheng/MyAIXd/projects/patients/' + self.patientID + '/3Ddose/exec/' + self.planname + '/Range_assigned.log'
        #     self.path2_3Danalog2 = '/u/ysheng/MyAIXd/projects/patients/' + self.patientID + '/3Ddose/exec/' + self.planname + '/Range_noassign.log'
        #     print(self.path2analog)
        # else:
        #     print('error input, check if you have input the path to TRiPlog or patient ID and plan name')
        if self.savename==None:
            self.savename=''
        if self.save2motionpath==None:
            self.save2motionpath = './'
        if self.save2rangepath==None:
            self.save2rangepath = './'

        self.path2_motion_processing_log = self.save2motionpath+'00_motion_ana_processing.log'
        self.path2_range_processing_log = self.save2rangepath+'00_range_ana_processing.log'

        self.voilist = []
        self.writelinesinfo=[]

    def fun_analysis_motion(self,motionlist):
        # dose_shown_in_gd is the dose written in the exec file, for SPHIC momi cases this value was
        # set to 3 for all plans.
        print('-m actived. start motion analysis, dat file written in ',self.save2motionpath)
        path2planmotionlogs = []
        find4Dlogs = [string for string in self.logdimlist if '4D' in string]
        if not(find4Dlogs):
            writeloginfo='no 4D motion file found, please check'
            relate_funs.writelog(self.path2_motion_processing_log, writeloginfo)
            sys.exit()
        for i in range(0,len(self.loglist)):
            if '4D' in self.logdimlist[i]:
                path2planmotionlogs.append(self.loglist[i]) # put 4D log list into path2planmotionlogs
        # write log
        writeloginfo = 'Start a new motion analysis\n running patient: ' + self.patientID + ' plan: ' + self.planname
        relate_funs.writelog(self.path2_motion_processing_log, writeloginfo)

        # write analysis data
        #writedata = 'ID planname Organ States'+(i for i in self.statelist)+'\n'
        writedata = '00_ID 00_Planname 00_OAR/Tname '
        for logfilelist in self.logdimlist:
            for States in self.statelist:
                if '4D' in logfilelist:
                    writedata += logfilelist+"_State"+States+' '
        writedata += '\n'

        for oarname in motionlist:
            writedata += ' ' + self.patientID + ' ' + self.planname + ' ' + oarname
            for path2planmotionlogfile in path2planmotionlogs:
                for statename in self.statelist:
                    motiondata = self.fun_motion_info(path2planmotionlogfile, oarname, statename)
                    writedata += motiondata
                    if motiondata==' 9999':
                        errorinfo='Please check:'+path2planmotionlogfile+' '+oarname+' phase'+statename
                        relate_funs.writelog(self.path2_motion_processing_log, errorinfo)
            writedata += '\n'

        # save info and analysis data
        save_motion_filename=self.save2motionpath+self.patientID+'_'+self.planname+'_'+self.savename+'_motion.txt'

        with open(save_motion_filename, 'w+') as savefileinfo:
            # savefileinfo.writelines('patientID plan VOI volume pre_dose parameter 3D 4D1 4D2 4D3 ...')
            savefileinfo.writelines(writedata)

    def fun_motion_info(self,path2planmotionlog,oarname,motionstate):
        average_motion=' 9999'
        with open(path2planmotionlog,'r') as mo_ran_log_to_ana:
            for data_to_ana in mo_ran_log_to_ana:
                data_to_ana_list=data_to_ana.split()
                determin_state='ref to state '+motionstate
                if determin_state in data_to_ana:
                    if oarname in data_to_ana_list:
                        average_motion=data_to_ana[data_to_ana.rfind(':')+1:-3]
        return average_motion
    def fun_analysis_range(self,rangefield):
        print('-r actived. start range analysis, dat file written in '+self.save2rangepath)
        # write log
        writeloginfo = 'Start a new range analysis\nrunning patient: ' + self.patientID + ' plan: ' + self.planname
        relate_funs.writelog(self.path2_range_processing_log, writeloginfo)
        # write analysis data
        writedata = '00_ID 00_Planname 00_field '
        for logfileNo in range(0, len(self.logdimlist)):
            if '3D' in self.logdimlist[logfileNo]:
                writedata += self.logdimlist[logfileNo] + 'mean_mm ' + self.logdimlist[logfileNo] + 'SD_mm '
            elif '4D' in self.logdimlist[logfileNo]:
                writedata += ' '.join(self.logdimlist[logfileNo] + 'mean_mm_state'+j+' ' + self.logdimlist[logfileNo] + 'SD_mm_state'+j \
                            for j in self.statelist)
        writedata += '\n'
        for fieldname in rangefield:
            writedata += self.patientID + ' ' + self.planname + ' field'
            writedata += fieldname
            for logfileNo in range(0,len(self.loglist)):
                if '3D' in self.logdimlist[logfileNo]:
                # write 3D plan range info for field N
                    average_range3D, standerror_range3D = self.fun_3Drange_info(fieldname,self.loglist[logfileNo])
                    writedata += average_range3D + standerror_range3D
                # write 4D range info for field N
                elif '4D' in self.logdimlist[logfileNo]:
                    average_range0, standerror_range0 = self.fun_4Drange_info(fieldname,self.loglist[logfileNo], '0')
                    writedata += average_range0 + standerror_range0
                    for statename in self.statelist:
                        if statename != '0':
                            average_range,standerror_range = self.fun_4Drange_info(fieldname,self.loglist[logfileNo], statename)
                            if average_range == '9999' or standerror_range == '9999':
                                errorinfo = 'either motion states or Field name wrongly defined. Please check.'
                                relate_funs.writelog(self.path2_range_processing_log, errorinfo)
                            writedata += average_range+standerror_range
                else:
                    errorinfo = 'Error logfile dimension not known!'
                    relate_funs.writelog(self.path2_range_processing_log, errorinfo)
            writedata += '\n'

        # save info and analysis data
        save_range_filename = self.save2rangepath + self.patientID + '_' + self.planname + '_' + self.savename + '_range.txt'
        with open(save_range_filename, 'w+') as savefileinfo:
            # savefileinfo.writelines('patientID plan VOI volume pre_dose parameter 3D 4D1 4D2 4D3 ...')
            savefileinfo.writelines(writedata)

    def fun_4Drange_info(self,fieldname,path2_4Danalog,statename):
        average_range='9999'
        standerror_range='9999'
        startline=0
        endline=0
        with open (path2_4Danalog,'r') as mo_ran_log_to_ana:
            datalineall=mo_ran_log_to_ana.readlines()
            dataline=0
            for data_to_ana in datalineall:
                dataline+=1
                if 'getH2Orange' in data_to_ana:
                    data_to_ana_list=data_to_ana.split()
                    if fieldname in data_to_ana_list:
                        startline=dataline
                if startline!=0 and '<TIME>' in data_to_ana:
                    endline=dataline
                    break
            dataline = 0
            for data_to_ana in datalineall:
                dataline += 1
                if dataline>startline and dataline<endline:
                    dertermin_state='Ranges for state '+statename
                    if dertermin_state in data_to_ana:
                        startline=dataline
                        endline=dataline+12
                        break
            dataline = 0
            for data_to_ana in datalineall:
                dataline += 1
                if dataline >= startline and dataline <= endline:
                    if 'mean' in data_to_ana:
                        average_range=data_to_ana[data_to_ana.rfind(':')+1:-3]
                    if 'std deviation' in data_to_ana:
                        standerror_range=data_to_ana[data_to_ana.rfind(':')+1:-3]
                        break
        return average_range,standerror_range
    def fun_3Drange_info(self,fieldname,path2_3Danalog):
        average_range='9999'
        standerror_range='9999'
        startline=0
        endline=0
        with open (path2_3Danalog,'r') as mo_ran_log_to_ana:
            datalineall=mo_ran_log_to_ana.readlines()
            dataline=0
            for data_to_ana in datalineall:
                dataline+=1
                if 'getH2Orange' in data_to_ana:
                    data_to_ana_list=data_to_ana.split()
                    if fieldname in data_to_ana_list:
                        startline=dataline
                        endline=startline+13
                if startline!=0 and '<TIME>' in data_to_ana:
                    endline=dataline
                    break
            dataline = 0
            for data_to_ana in datalineall:
                dataline += 1
                if dataline>startline and dataline<endline:
                    if 'mean' in data_to_ana:
                        average_range=data_to_ana[data_to_ana.rfind(':')+1:-3]
                    if 'std deviation' in data_to_ana:
                        standerror_range=data_to_ana[data_to_ana.rfind(':')+1:-3]
                        break
        return average_range,standerror_range