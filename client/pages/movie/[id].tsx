import Avatar from "@material-ui/core/Avatar"
import Badge from "@material-ui/core/Badge"
import Chip from "@material-ui/core/Chip"
import CircularProgress from "@material-ui/core/CircularProgress"
import CssBaseline from "@material-ui/core/CssBaseline"
import Divider from "@material-ui/core/Divider"
import Grid from "@material-ui/core/Grid"
import Paper from "@material-ui/core/Paper"
import Slide from "@material-ui/core/Slide"
import Snackbar from "@material-ui/core/Snackbar"
import { createStyles, makeStyles } from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import MovieIcon from "@material-ui/icons/Movie"
import TheatersIcon from "@material-ui/icons/Theaters"
import { AxiosResponse } from "axios"
import { GetServerSideProps, NextPage } from "next"
import { useCallback, useEffect, useReducer } from "react"
import { ApiCompleteMovieResponse, ApiCompleteMovieResult, ImdbApi } from "services/api.imdb"
import { AnalysisResponse, SentimentAnalysisApi } from "services/api.sentiment-analysis"
import { analysisReducer } from "services/custom.reducers"

const useStyles = makeStyles(theme =>
	createStyles({
		root: {
			height: "100vh",
		},
		image: {
			backgroundRepeat: "no-repeat",
			backgroundSize: "contain",
			backgroundPosition: "center",
		},
		paper: {
			margin: theme.spacing(8, 4),
			display: "flex",
			flexDirection: "column",
			alignItems: "center",
		},
		badge: {
			marginRight: theme.spacing(2),
		},
		divider: {
			margin: theme.spacing(2),
		},
		chips: {
			display: "flex",
			justifyContent: "center",
			flexWrap: "wrap",
			"& > *": {
				margin: theme.spacing(0.5),
			},
		},
	})
)

export interface IMovieProps {
	movie: ApiCompleteMovieResult
}

const Movie: NextPage<IMovieProps> = ({ movie }) => {
	const classes = useStyles()
	const [movieAnalysis, setMovieAnalysis] = useReducer(analysisReducer, { state: "LOADING" })

	useEffect(() => {
		;(async () => {
			const { data }: AxiosResponse<AnalysisResponse> = await SentimentAnalysisApi(movie.Title)
			setMovieAnalysis(
				"error" in data ? { type: "ERROR", ...data } : { type: "STORE", review: data }
			)
			console.log(data)
		})()
	}, [SentimentAnalysisApi, setMovieAnalysis])

	const renderAnalysis = useCallback(() => {
		if (movieAnalysis.state === "LOADING") return <CircularProgress color='secondary' />
		else if (movieAnalysis.state === "ERROR")
			return (
				<Snackbar
					open={true}
					anchorOrigin={{
						horizontal: "left",
						vertical: "bottom",
					}}
					message={movieAnalysis.error[0] ?? "IMDB page error"}
					TransitionComponent={props => <Slide {...props} direction='left' />}
				/>
			)
		else
			return (
				<Paper color='primary'>
					<Typography color='primary' paragraph>
						Sentiment Analysis
					</Typography>
					<Typography color='secondary' paragraph>
						Positive Review : {movieAnalysis.review.positiveReviewPercentage} %
					</Typography>
					<Typography color='secondary' paragraph>
						Result : {movieAnalysis.review.message}
					</Typography>
				</Paper>
			)
	}, [movieAnalysis])

	console.log(movie)
	return (
		<Grid container component='main' className={classes.root}>
			<CssBaseline />
			<Grid
				item
				xs={false}
				sm={4}
				className={classes.image}
				style={{ backgroundImage: `url(${movie.Poster})` }}
			/>
			<Grid item xs={12} sm={8} component={Paper} elevation={6} square>
				<div className={classes.paper}>
					<Typography component='h1' variant='h4'>
						<Badge
							variant='dot'
							className={classes.badge}
							color={movie.Type === "series" ? "primary" : "secondary"}
						>
							{movie.Type === "movie" ? <TheatersIcon /> : <MovieIcon />}
						</Badge>
						{movie.Title}
					</Typography>
					<Divider className={classes.divider} variant='middle' light />
					<div className={classes.chips}>
						{movie.Genre.split(", ").map((genre, idx) => (
							<Chip
								key={idx}
								size='small'
								avatar={<Avatar title='G' />}
								label={genre}
								clickable
								color='primary'
							/>
						))}
					</div>
					<Divider className={classes.divider} variant='middle' light />
					<Typography paragraph>{movie.Plot}</Typography>
					<Divider className={classes.divider} variant='middle' light />
					{renderAnalysis()}
				</div>
			</Grid>
		</Grid>
	)
}

export const getServerSideProps: GetServerSideProps<IMovieProps, { id: string }> = async ctx => {
	const { data }: AxiosResponse<ApiCompleteMovieResponse> = await ImdbApi({
		params: { plot: "full", i: ctx.params!.id },
	})
	if (typeof data === "string" || data.Response === "False") return { notFound: true }
	return { props: { movie: data } }
}
export default Movie
