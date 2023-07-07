// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// function WeatherComponent() {
//   const [weather, setWeather] = useState(null);

//   useEffect(() => {
//     // 使用axios发起GET请求
//     axios.get('http://127.0.0.1:8000/api/current-weather/')
//       .then(response => {
//         // 在promise resolve后，将结果保存在状态中
//         setWeather(response.data);
//       })
//       .catch(error => {
//         // 在发生错误时进行处理
//         console.error('Error fetching weather data:', error);
//       });
//   }, []); // 空数组表示这个useEffect只在组件首次渲染时运行

//   // 在请求完成并且数据已经保存在状态中后显示结果
//   return weather ? (
//     <div>
//       <h1>Current Weather:</h1>
//       <p>{JSON.stringify(weather)}</p>
//     </div>
//   ) : (
//     // 在数据加载中时显示一个加载信息
//     <div>Loading...</div>
//   );
// }

// export default WeatherComponent;


import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSun, faCloud, faBolt, faSnowflake, faCloudRain, faSmog } from "@fortawesome/free-solid-svg-icons";

function WeatherComponent() {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    // 使用axios发起GET请求
    axios.get('http://127.0.0.1:8000/api/current-weather/')
      .then(response => {
        // 在promise resolve后，将结果保存在状态中
        setWeather(response.data);
      })
      .catch(error => {
        // 在发生错误时进行处理
        console.error('Error fetching weather data:', error);
      });
  }, []); // 空数组表示这个useEffect只在组件首次渲染时运行

  // 在请求完成并且数据已经保存在状态中后显示结果
  return weather ? (
    <div>
      {/* <h1>Current Weather:</h1> */}
      <p>{JSON.stringify(weather)}</p>
      {/* 根据天气图标选择适当的图标 */}
      {weather.weather[0].icon === '01d' && <FontAwesomeIcon icon={faSun} />}
      {weather.weather[0].icon === '02d' && <FontAwesomeIcon icon={faCloud} />}
      {weather.weather[0].icon === '03d' && <FontAwesomeIcon icon={faCloud} />}
      {weather.weather[0].icon === '04d' && <FontAwesomeIcon icon={faCloud} />}
      {weather.weather[0].icon === '09d' && <FontAwesomeIcon icon={faRain} />}
      {weather.weather[0].icon === '10d' && <FontAwesomeIcon icon={faRain} />}
      {weather.weather[0].icon === '11d' && <FontAwesomeIcon icon={faBolt} />}
      {weather.weather[0].icon === '13d' && <FontAwesomeIcon icon={faSnowflake} />}
      {weather.weather[0].icon === '50d' && <FontAwesomeIcon icon={faSmog} />}
    </div>
  ) : (
    // 在数据加载中时显示一个加载信息
    <div>Loading...</div>
  );
}

export default WeatherComponent;

