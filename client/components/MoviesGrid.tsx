import { createStyles, makeStyles } from "@material-ui/core"
import Button from "@material-ui/core/Button"
import Card from "@material-ui/core/Card"
import CardActionArea from "@material-ui/core/CardActionArea"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import CardMedia from "@material-ui/core/CardMedia"
import Grid from "@material-ui/core/Grid"
import Grow from "@material-ui/core/Grow"
import IconButton from "@material-ui/core/IconButton"
import Paper from "@material-ui/core/Paper"
import Tooltip from "@material-ui/core/Tooltip"
import Typography from "@material-ui/core/Typography"
import MovieIcon from "@material-ui/icons/Movie"
import TheatersIcon from "@material-ui/icons/Theaters"
import { NextPage } from "next"
import { useRouter } from "next/router"
import { ApiSearchResult } from "services/api.imdb"
import { useCallback } from "react"

const useStyles = makeStyles(() =>
	createStyles({
		root: {
			paddingTop: 20,
		},
	})
)

export interface IMoviesGridProps {
	movies: ApiSearchResult[]
}

export const MoviesGrid: NextPage<IMoviesGridProps> = ({ movies }) => {
	const classes = useStyles()
	const router = useRouter()

	const onCardClick = useCallback(
		(imdbID: string) => () => router.push(`movie/${imdbID}`),
		[router]
	)

	return (
		<Grid container spacing={2} className={classes.root}>
			{movies.map(({ imdbID, Title, Poster, Type, Year }, idx) => (
				<Grid item key={imdbID} xs={12} sm={6} md={4} lg={3}>
					<Grow in={true} timeout={idx * 500}>
						<Paper elevation={10}>
							<Card onClick={onCardClick(imdbID)}>
								<CardActionArea>
									<Tooltip title={Year} arrow>
										<CardMedia component='img' alt={Title} image={Poster} />
									</Tooltip>
									<CardContent>
										<Typography gutterBottom variant='h5' component='h2'>
											{Title}
										</Typography>
									</CardContent>
								</CardActionArea>
								<CardActions>
									<Button size='small' color='primary'>
										Learn More
									</Button>
									<IconButton color={Type === "series" ? "primary" : "secondary"}>
										{Type === "movie" ? <TheatersIcon /> : <MovieIcon />}
									</IconButton>
								</CardActions>
							</Card>
						</Paper>
					</Grow>
				</Grid>
			))}
		</Grid>
	)
}
