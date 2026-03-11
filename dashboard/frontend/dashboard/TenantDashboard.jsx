import React, { useEffect, useState } from "react";

function TenantDashboard() {

  const [domains, setDomains] = useState([]);

  useEffect(() => {

    fetch("/domains")
      .then(res => res.json())
      .then(data => setDomains(data));

  }, []);

  return (

    <div>

      <h2>Monitored Domains</h2>

      <ul>
        {domains.map(d => (
          <li key={d}>{d}</li>
        ))}
      </ul>

    </div>

  );
}

export default TenantDashboard;