import React, { useEffect, useState } from "react";
import AssetTable from "./AssetTable";

function Dashboard() {

  const [assets, setAssets] = useState([]);

  useEffect(() => {

    fetch("http://localhost:8000/assets")
      .then(res => res.json())
      .then(data => setAssets(data));

  }, []);

  return (
    <div>
      <h2>Discovered Assets</h2>
      <AssetTable assets={assets} />
    </div>
  );
}

export default Dashboard;