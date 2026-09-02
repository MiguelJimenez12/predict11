import { useEffect, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const demoTeams = [
  { id: 2282, name: 'Pumas UNAM' }, { id: 2285, name: 'Club América' },
  { id: 2279, name: 'Guadalajara' }, { id: 2295, name: 'Cruz Azul' },
  { id: 2284, name: 'Monterrey' }, { id: 2283, name: 'Tigres UANL' },
]

function App() {
  const [teams, setTeams] = useState(demoTeams)
  const [homeTeam, setHomeTeam] = useState(demoTeams[0].id)
  const [awayTeam, setAwayTeam] = useState(demoTeams[1].id)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [notice, setNotice] = useState('')

  useEffect(() => {
    fetch(`${API_URL}/teams/`)
      .then((response) => { if (!response.ok) throw new Error(); return response.json() })
      .then((data) => {
        if (data.length) { setTeams(data); setHomeTeam(data[0].id); setAwayTeam(data[1]?.id ?? data[0].id) }
      })
      .catch(() => setNotice('Mostrando equipos de demostración. Conecta la API para usar datos en vivo.'))
  }, [])

  async function predict(event) {
    event.preventDefault()
    if (homeTeam === awayTeam) { setNotice('Selecciona dos equipos diferentes.'); return }
    setLoading(true); setNotice(''); setPrediction(null)
    try {
      const response = await fetch(`${API_URL}/predict/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ home_team: Number(homeTeam), away_team: Number(awayTeam) }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'No fue posible generar la predicción.')
      setPrediction(data)
    } catch (error) { setNotice(error.message) } finally { setLoading(false) }
  }

  return (
    <main>
      <nav><a className="brand" href="#top"><span>P11</span> Predict11</a><a className="nav-link" href="http://localhost:8000/docs" target="_blank">API Docs ↗</a></nav>
      <section className="hero" id="top">
        <div className="eyebrow"><i /> Liga MX · Datos + modelo estadístico</div>
        <h1>El partido empieza<br />antes del silbatazo.</h1>
        <p>Compara el rendimiento de dos equipos y obtén una predicción transparente en segundos.</p>
      </section>
      <section className="predictor">
        <form onSubmit={predict}>
          <div className="team-field"><label htmlFor="home">LOCAL</label><select id="home" value={homeTeam} onChange={(e) => setHomeTeam(Number(e.target.value))}>{teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}</select></div>
          <div className="versus">VS</div>
          <div className="team-field"><label htmlFor="away">VISITANTE</label><select id="away" value={awayTeam} onChange={(e) => setAwayTeam(Number(e.target.value))}>{teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}</select></div>
          <button disabled={loading}>{loading ? 'ANALIZANDO…' : 'GENERAR PREDICCIÓN →'}</button>
        </form>
        {notice && <div className="notice">{notice}</div>}
        {prediction && <article className="result">
          <header><div><small>PRONÓSTICO DEL MODELO</small><h2>{prediction.home_team} <em>{prediction.predicted_score}</em> {prediction.away_team}</h2></div><span className="confidence">Confianza {prediction.confidence}</span></header>
          <div className="probabilities">{[['Victoria local', prediction.home_win_probability], ['Empate', prediction.draw_probability], ['Victoria visitante', prediction.away_win_probability]].map(([label, value]) => <div className="probability" key={label}><strong>{value}%</strong><span>{label}</span><div><i style={{ width: `${value}%` }} /></div></div>)}</div>
          <div className="explanation"><h3>¿Por qué este resultado?</h3><ul>{prediction.explanation.map((item) => <li key={item}>{item}</li>)}</ul></div>
        </article>}
      </section>
      <section className="method"><span>01</span><div><h3>Forma reciente</h3><p>Victorias, derrotas y puntos por partido.</p></div><span>02</span><div><h3>Potencia ofensiva</h3><p>Goles anotados, recibidos y porterías en cero.</p></div><span>03</span><div><h3>Historial directo</h3><p>El peso de los últimos enfrentamientos entre ambos.</p></div></section>
      <footer><b>Predict11</b><span>Una predicción es una estimación, no una garantía.</span><span>v1.0</span></footer>
    </main>
  )
}

export default App
