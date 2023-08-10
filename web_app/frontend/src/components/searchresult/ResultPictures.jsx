import colours from "../dummydata/colours.js";

export function getImageUrlSmallById(locationId) {
  // console.log("LOOK AT THIS LOCATION ID", locationId)
  const foundObject = colours.find((item) => item.location_id === locationId);

  // return foundObject ? foundObject.image_url_small : null;
  return foundObject ? foundObject.image_url : null;
}
