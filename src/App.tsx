import { useState, useEffect } from "react"
import ContentTable from "./ContentTable"
import "./style.css"

const fetchData = async (path: string): Promise<string[]> => {
  const response: Response = await fetch(`${import.meta.env.BASE_URL}${path}`)
  const data: string = await response.text()
  const words: string[] = data.split("\n")
  return words
}

const shuffleArray = (array: string[]): string[] => array
  .map(value => ({ value, sort: Math.random() }))
  .sort((a, b) => a.sort - b.sort)
  .map(({ value }) => value)

const handleCells = (): void => {
  const table = document.querySelector("table")
  if (!table) return

  const tr = table.querySelectorAll("tr")
  const td = (row: HTMLElement): NodeListOf<HTMLTableCellElement> => row.querySelectorAll("td")

  const rows = Array.from(tr)
  const cols = Array.from(tr).map(row => Array.from(td(row)))

  // Rows and columns
  rows.forEach(row => td(row).forEach(el => el.classList.remove("won")))
  rows.forEach((row, i) => {
    if (row.querySelectorAll("td.selected").length === cols[i].length)
      td(row).forEach(el => el.classList.add("won"))
    if (cols.every(col => col[i]?.classList.contains("selected")))
      cols.forEach(col => col[i]?.classList.add("won"))
  })

  // Diagonals
  if (rows.every((row, i) => td(row)[i]?.classList.contains("selected")))
    rows.forEach((row, i) => td(row)[i].classList.add("won"))
  if (rows.every((row, i) => td(row)[cols.length - 1 - i]?.classList.contains("selected")))
    rows.forEach((row, i) => td(row)[cols.length - 1 - i].classList.add("won"))
}

document.addEventListener("click", e => {
  const element = (e.target as HTMLElement)?.closest("td") as HTMLElement
  if (!element) return

  element.classList.toggle("selected")
  handleCells()
})

const App = () => {
  const [showComponent, setShowComponent] = useState(false)
  const [words, setWords] = useState<string[]>([])
  const [dataFetched, setDataFetched] = useState(false)

  useEffect(() => {
    if (showComponent && !dataFetched) fetchData("/prompts/vita.txt") // Currently by default
      .then(data => {
        setWords(shuffleArray(data).slice(0, 25))
        setDataFetched(true)
      })
  }, [showComponent, dataFetched])

  const handleStartClick = (): void => {
    document.querySelectorAll("td").forEach(el => {
      el.classList.remove("selected")
      el.classList.remove("won")
    })
    dataFetched ? setWords(shuffleArray(words).slice(0, 25)) : setShowComponent(true)
  }

  return (
    <>
      <h3>Pirmajam, kas dabū bingo, ir jāiebļaujas, lai uzvarētu</h3>
      {showComponent && <ContentTable words={words} />}
      <div className="btn" onClick={handleStartClick}>{dataFetched ? "UPDATE" : "START"}</div>
    </>
  )
}

export default App