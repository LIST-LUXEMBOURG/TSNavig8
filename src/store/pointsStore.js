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
        ADD_LIDAR_DATA(lidarData) {
            this.lidarData = lidarData
        }
    }
})
