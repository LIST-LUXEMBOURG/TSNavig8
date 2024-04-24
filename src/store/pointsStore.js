/*
  © 2024 - Luxembourg Institute of Science and Technology. All Rights Reserved
  This program is licensed under AGPL V3.0 License -  https://www.gnu.org/licenses/agpl-3.0.txt
*/
import { defineStore } from "pinia";

export const usePointsStore = defineStore('pointsStore', {
    state: () => ({
        lidarData: [],
    })
    ,
    getters: {
        getLidarData: state => state.lidarData,
    },
    actions: {
        setLidarData(lidarData_) {
            this.lidarData = lidarData_
        }
    }
})
