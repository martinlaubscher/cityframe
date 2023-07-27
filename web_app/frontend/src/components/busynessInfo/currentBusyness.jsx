import axios from '@/axiosConfig';

export async function getAllBusyness() {
    try {
        const response = await // Notice：de-comment in final version
            // axios.get("/api/current-busyness");
            axios.get(`/api/current-busyness`);
        //Notice：comment before commit
        //   axios.get('http://127.0.0.1:8000/api/current-busyness');
        console.log(response.data); // Add this line to debug your API response
        return response.data;
    } catch (error) {
        console.error("There was an error retrieving the data: ", error);
    }
}

export function filterBusyness(busynessLevel, zones) {
    return Object.keys(zones).filter((zone) => zones[zone] === busynessLevel);
}
