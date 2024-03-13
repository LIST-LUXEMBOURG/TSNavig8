import {defineStore} from "pinia";

export const usePointsStore = defineStore('lidarData', {
    state: () => ({
            lidarData: [],
        })
    ,
    getters: {
        getLidarData: state => state.lidarData,
    },
    actions: {
        setLidarData(lidarData) {
            this.lidarData = lidarData
            console.log("lidarData: " + JSON.stringify(this.getLidarData))
        }
    }
})
