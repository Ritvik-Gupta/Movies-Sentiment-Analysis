import { Reducer } from "react"
import { ApiSearchResult } from "./api.imdb"

type InputAction = { type: "CHANGE"; value: string }

export const inputReducer: Reducer<string, InputAction> = (_, action) => {
	switch (action.type) {
		case "CHANGE":
			return action.value
	}
}

type ApiSearchAction =
	| { type: "ADD"; search: ApiSearchResult[] }
	| { type: "ERROR"; error: string }
	| { type: "LOADING" | "RESET" | "CONTINUE" }
type ApiSearchState = { search: ApiSearchResult[]; error?: string; isLoading: boolean }

export const apiSearchReducer: Reducer<ApiSearchState, ApiSearchAction> = (prevState, action) => {
	switch (action.type) {
		case "ADD":
			const search: ApiSearchResult[] = []
			action.search.concat(prevState.search).forEach(movie => {
				if (!search.some(({ imdbID }) => movie.imdbID === imdbID)) search.push(movie)
			})
			return { search, isLoading: false }
		case "ERROR":
			return { ...prevState, error: action.error, isLoading: false }
		case "LOADING":
			return { ...prevState, isLoading: true }
		case "RESET":
			return { search: [], isLoading: false }
		case "CONTINUE":
			return { search: prevState.search, isLoading: false }
	}
}
