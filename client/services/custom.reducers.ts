import { Reducer } from "react"
import { ApiSearchResult } from "./api.imdb"
import { AnalysisError, AnalysisResponse, AnalysisSuccess } from "./api.sentiment-analysis"

type InputAction = { type: "CHANGE"; value: string } | { type: "CLEAR" }

export const inputReducer: Reducer<string, InputAction> = (_, action) => {
	switch (action.type) {
		case "CHANGE":
			return action.value
		case "CLEAR":
			return ""
	}
}

type ApiSearchAction =
	| { type: "ADD"; search: ApiSearchResult[] }
	| { type: "ERROR"; error: string }
	| { type: "LOADING" | "CONTINUE" }
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
		case "CONTINUE":
			return { search: prevState.search, isLoading: false }
	}
}

type AnalysisAction =
	| { type: "STORE"; review: AnalysisSuccess }
	| ({ type: "ERROR" } & AnalysisError)
type AnalysisState =
	| { state: "LOADING" }
	| ({ state: "ERROR" } & AnalysisError)
	| { state: "REVIEW"; review: AnalysisSuccess }

export const analysisReducer: Reducer<AnalysisState, AnalysisAction> = (_, action) => {
	switch (action.type) {
		case "STORE":
			return { state: "REVIEW", review: action.review }
		case "ERROR":
			return { state: "ERROR", error: action.error }
	}
}
