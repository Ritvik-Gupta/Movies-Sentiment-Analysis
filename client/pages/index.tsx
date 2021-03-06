import Backdrop from "@material-ui/core/Backdrop"
import CircularProgress from "@material-ui/core/CircularProgress"
import Container from "@material-ui/core/Container"
import Slide from "@material-ui/core/Slide"
import Snackbar from "@material-ui/core/Snackbar"
import { createStyles, makeStyles } from "@material-ui/core/styles"
import TextField from "@material-ui/core/TextField"
import { AxiosResponse } from "axios"
import { MoviesGrid } from "components/MoviesGrid"
import { NextPage } from "next"
import { FormEvent, useCallback, useReducer } from "react"
import { ApiSearchResponse, ImdbApi } from "services/api.imdb"
import { apiSearchReducer, inputReducer } from "services/custom.reducers"

const useStyles = makeStyles(theme =>
	createStyles({
		backdrop: {
			zIndex: theme.zIndex.drawer + 1,
			color: "#fff",
		},
		container: {
			paddingTop: 15,
		},
	})
)

export interface IIndexProps {}

const Index: NextPage<IIndexProps> = ({}) => {
	const classes = useStyles()

	const [movieName, setMovieName] = useReducer(inputReducer, "")
	const [movies, setMovies] = useReducer(apiSearchReducer, { search: [], isLoading: false })

	const onFormSubmit = useCallback(
		async (event: FormEvent<HTMLFormElement>) => {
			event.preventDefault()
			setMovies({ type: "LOADING" })

			const { data }: AxiosResponse<ApiSearchResponse> = await ImdbApi({ params: { s: movieName } })

			setMovies(
				data.Response == "True"
					? { type: "ADD", search: data.Search }
					: { type: "ERROR", error: data.Error }
			)
			setMovieName({ type: "CLEAR" })
		},
		[movieName, ImdbApi, setMovies, setMovieName]
	)

	return (
		<Container className={classes.container} fixed>
			<form onSubmit={onFormSubmit}>
				<TextField
					color='secondary'
					fullWidth
					value={movieName}
					label='Movie Name'
					variant='filled'
					onChange={event => {
						setMovies({ type: "CONTINUE" })
						setMovieName({ type: "CHANGE", value: event.target.value })
					}}
					disabled={movies.isLoading}
				/>
			</form>
			<Backdrop className={classes.backdrop} open={movies.isLoading}>
				<CircularProgress color='secondary' />
			</Backdrop>
			<Snackbar
				open={movies.error !== undefined}
				autoHideDuration={5000}
				onClose={(_, reason) => {
					if (reason === "timeout") setMovies({ type: "CONTINUE" })
				}}
				anchorOrigin={{
					horizontal: "left",
					vertical: "bottom",
				}}
				message={movies.error}
				TransitionComponent={props => <Slide {...props} direction='left' />}
			/>
			<MoviesGrid movies={movies.search} />
		</Container>
	)
}

export default Index
