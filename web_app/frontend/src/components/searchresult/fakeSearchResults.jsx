import fakeData from './fakeSearchResults.json';

export function fetchFakeSearchResults() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(fakeData);
    }, 500);
  });
}
