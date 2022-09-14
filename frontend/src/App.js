import React from 'react'
import BasicTabs from './component/Basictaps';

function App() {
  // const [data, setData] = useState(0)

  // useEffect(() => {
  //   fetch('http://localhost:5000/', {
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Accept': 'application/json'
  //     }
  //   })
  //     .then(res => res.json())
  //     .then(data => {
  //       setData(data.data)
  //       console.log(data)
  //     })
  //     .catch(error => {
  //       console.log(error)
  //     })
  // }, [])

  return (
    <BasicTabs/>
  );
}

export default App;
