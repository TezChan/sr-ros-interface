# -*- coding: utf-8 -*-
##
# Copyright 2011 Shadow Robot Company Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#By: Emilie JEAN-BAPTISTE
##Date:24 Juin 2011

import roslib; roslib.load_manifest('sr_automatic_pid_tuning')
import rospy

import numpy as np
from sr_automatic_pid_tuning.optimization_algorithm.Genetic_Algorithm.movement.partial_movements import Partial_Movements


class Partial_Movement_Small_Steps(Partial_Movements):
    def __init__(self,joint_name, robot_lib):
        Partial_Movements.__init__(self,joint_name, robot_lib)
        self.number_steps=95
        self.movement_name="Little Steps"
        self.Target_inc=5
        self.ps=[]
        self.sequences=[]
        return


    def compute_data(self,itr):
	"""
	Will compute the chosen movement
	@return: targets for sendupdate
	"""
	ptn=5*itr
	self.sequences.append(ptn)
	if itr>=1:
	    if itr%5==0:
		self.ps.append("add")
		itr=len(self.ps)
	    else:
		itr=len(self.ps)


	return self.sequences[itr]


