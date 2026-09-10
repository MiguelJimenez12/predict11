import { useEffect, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const fallbackLeagues = [{ slug: 'liga-mx', name: 'Liga MX' }]

function App() {
  const [leagues, setLeagues] = useState(fallbackLeagues)
  const [league, setLeague] = useState('liga-mx')
  const [teams, setTeams] = useState([])
  const [homeTeam, setHomeTeam] = useState('')
  const [awayTeam, setAwayTeam] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)
  const [notice, setNotice] = useState('')

  useEffect(() => {
    fetch(`${API_URL}/leagues/`)
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then(setLeagues)
      .catch(() => setNotice('No fue posible cargar el catálogo de ligas.'))
  }, [])

  useEffect(() => {
    fetch(`${API_URL}/leagues/${league}/teams`)
      .then(async (response) => {
        const data = await response.json()
        if (!response.ok) throw new Error(data.detail || 'No fue posible cargar los equipos.')
        return data
      })
      .then((data) => {
        setTeams(data)
        setHomeTeam(String(data[0]?.id || ''))
        setAwayTeam(String(data[1]?.id || ''))
      })
      .catch((error) => { setTeams([]); setNotice(error.message) })
      .finally(() => setLoading(false))
  }, [league])

  function selectLeague(slug) {
    setLoading(true)
    setPrediction(null)
    setNotice('')
    setLeague(slug)
  }

  async function predict(event) {
    event.preventDefault()
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      setNotice('Selecciona dos equipos diferentes.')
      return
    }
    setLoading(true)
    setNotice('')
    setPrediction(null)
    const home = teams.find((team) => String(team.id) === homeTeam)
    const away = teams.find((team) => String(team.id) === awayTeam)
    const isLigaMx = league === 'liga-mx'
    const endpoint = isLigaMx ? '/predict/' : '/predictions/'
    const body = isLigaMx
      ? { home_team: Number(homeTeam), away_team: Number(awayTeam) }
      : { league, home_team: home.name, away_team: away.name }

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'No fue posible generar la predicción.')
      setPrediction(isLigaMx ? data : {
        home_team: data.home_team,
        away_team: data.away_team,
        home_win_probability: (data.home_win * 100).toFixed(1),
        draw_probability: (data.draw * 100).toFixed(1),
        away_win_probability: (data.away_win * 100).toFixed(1),
        predicted_score: '1X2',
        confidence: data.confidence,
        explanation: [
          ...(data.coverage === 'baseline' ? ['Champions League usa una comparativa base: todavía no hay un modelo histórico validado para esta competencia.'] : []),
          ...(data.coverage === 'partial' ? ['Al menos un equipo no aparece en las cinco temporadas históricas; se aplicó una referencia promedio de su liga.'] : []),
          ...(data.coverage === 'historical' ? ['Modelo entrenado cronológicamente con cinco temporadas históricas.'] : []),
          'Considera Elo, últimos cinco partidos, goles y rendimiento local/visitante.',
          data.model_version ? `Versión del modelo: ${data.model_version}` : 'Resultado de referencia, no de modelo entrenado.',
        ],
      })
    } catch (error) {
      setNotice(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main>
      <nav><a className="brand" href="#top"><span>P11</span> Predict11</a><a className="nav-link" href={`${API_URL}/docs`} target="_blank">API Docs ↗</a></nav>
      <section className="hero" id="top"><div className="eyebrow"><i /> Siete competiciones · datos abiertos + ML</div><h1>El partido empieza<br />antes del silbatazo.</h1><p>Compara equipos de las principales ligas y obtén probabilidades evaluadas con datos históricos.</p></section>
      <section className="league-picker" aria-label="Seleccionar liga">
        {leagues.map((item) => <button className={league === item.slug ? 'active' : ''} key={item.slug} onClick={() => selectLeague(item.slug)}>{item.name}</button>)}
      </section>
      <section className="predictor">
        <form onSubmit={predict}>
          <div className="team-field"><label htmlFor="home">LOCAL</label><select id="home" value={homeTeam} onChange={(event) => setHomeTeam(event.target.value)} disabled={!teams.length}>{teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}</select></div>
          <div className="versus">VS</div>
          <div className="team-field"><label htmlFor="away">VISITANTE</label><select id="away" value={awayTeam} onChange={(event) => setAwayTeam(event.target.value)} disabled={!teams.length}>{teams.map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}</select></div>
          <button disabled={loading || teams.length < 2}>{loading ? 'ANALIZANDO…' : 'GENERAR PREDICCIÓN →'}</button>
        </form>
        {notice && <div className="notice">{notice}</div>}
        {prediction && <article className="result"><header><div><small>PRONÓSTICO DEL MODELO</small><h2>{prediction.home_team} <em>{prediction.predicted_score}</em> {prediction.away_team}</h2></div><span className="confidence">Confianza {prediction.confidence}</span></header><div className="probabilities">{[['Victoria local', prediction.home_win_probability], ['Empate', prediction.draw_probability], ['Victoria visitante', prediction.away_win_probability]].map(([label, value]) => <div className="probability" key={label}><strong>{value}%</strong><span>{label}</span><div><i style={{ width: `${value}%` }} /></div></div>)}</div><div className="explanation"><h3>¿Por qué este resultado?</h3><ul>{prediction.explanation.map((item) => <li key={item}>{item}</li>)}</ul></div></article>}
      </section>
      <section className="method"><span>01</span><div><h3>Forma reciente</h3><p>Los últimos cinco partidos se calculan sin mirar al futuro.</p></div><span>02</span><div><h3>Fuerza y goles</h3><p>Elo, ataque, defensa y desempeño local/visitante.</p></div><span>03</span><div><h3>Evaluación real</h3><p>Accuracy, log loss, Brier score y matriz de confusión.</p></div></section>
      <footer><b>Predict11</b><span>Una predicción es una estimación, no una garantía.</span><span>v2.0</span></footer>
    </main>
  )
}

export default App
