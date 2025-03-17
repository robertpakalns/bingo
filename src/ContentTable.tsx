const ContentTable = ({ words }: { words: string[] }) =>
    <table>
        <tbody>
            {Array.from({ length: 5 }, (_, row) => (
                <tr key={row}>
                    {Array.from({ length: 5 }, (_, column) => (
                        <td key={column}>{words[row * 5 + column]}</td>
                    ))}
                </tr>
            ))}
        </tbody>
    </table>

// Input: words: string[]
// Output: 5x5 table with words

export default ContentTable