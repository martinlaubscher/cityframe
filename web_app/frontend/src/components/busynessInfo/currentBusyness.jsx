import axios from "@/axiosConfig";

export async function getAllBusyness() {
  try {
    const response = await axios.get(`/api/current-busyness`);

    console.log(response.data); // Add this line to debug API response
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
