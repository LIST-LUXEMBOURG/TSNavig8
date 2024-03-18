import {defineStore} from "pinia";

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
            // console.log("lidarData: " + JSON.stringify(this.getLidarData))
        }
    }
})
