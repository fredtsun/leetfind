import React from "react";
import "./App.css";
import {
    Table,
    TableContainer,
    TableCell,
    Paper,
    TextField,
    TableBody,
    TableHead,
    TableRow,
} from "@material-ui/core";

const SEARCH_URL = "http://localhost:8000";

interface LeetcodeProblem {
    question_id: number;
    url: string;
    title: string;
}

interface SearchTableProps {
    headers: string[];
}

const Headers = (prop: SearchTableProps) => {
    return (
        <TableHead>
            <TableRow>
                {prop.headers.map((title) => (
                    <TableCell align="left">{title}</TableCell>
                ))}
            </TableRow>
        </TableHead>
    );
};

class SearchTable extends React.Component<{}, { data: LeetcodeProblem[] }> {
    constructor(props: {}) {
        super(props);
        this.state = { data: [] };
        this.searchTermChange = this.searchTermChange.bind(this);
    }

    async searchTermChange(event: React.ChangeEvent<HTMLInputElement>) {
        const input = event.target.value;
        if (!input) {
            this.setState({ data: [] });
            return;
        }
        const resp = await fetch(`${SEARCH_URL}/${input}`);
        const json = await resp.json();
        if ("data" in json) {
            this.setState({ data: json["data"] });
        }
    }

    render() {
        return (
            <div>
                <form autoComplete="off">
                    <TextField
                        id="standard-basic"
                        label="Search for keywords"
                        onChange={this.searchTermChange}
                    />
                </form>
                <TableContainer component={Paper}>
                    <Table size="small" aria-label="problems table">
                        <Headers headers={["ID", "Title", "URL"]} />
                        <TableBody>
                            {this.state.data.map((row) => {
                                return (
                                    <TableRow key={row.question_id}>
                                        <TableCell align="left">
                                            {row.question_id}
                                        </TableCell>
                                        <TableCell align="left">
                                            {row.title}
                                        </TableCell>
                                        <TableCell align="left">
                                            <a href={row.url}>{row.url}</a>
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        );
    }
}

function App() {
    return (
        <div className="App">
            <header>Leetfind</header>
            <SearchTable />
        </div>
    );
}

export default App;
