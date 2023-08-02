import axios from "@/axiosConfig";

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
// export function filterBusyness(busynessLevel, zones) {
//     const result = {};
//     for (let zone in zones) {
//         const level = zones[zone];
//         if (!(level in result)) {
//             result[level] = [];
//         }
//         result[level].push(zone);
//     }
//     return result;
// }

export function filterBusyness(busynessLevel, zones) {
  const busynessZones = Object.keys(zones).reduce((acc, zone) => {
    const level = zones[zone];
    if (!acc[level]) {
      acc[level] = [];
    }
    acc[level].push(zone);
    return acc;
  }, {});

  // return user expected busyness: zones
  return { [busynessLevel]: busynessZones[busynessLevel] };
}
