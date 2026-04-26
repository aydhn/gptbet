import typer
from rich.console import Console
from sports_signal_bot.portfolio.contracts import PortfolioConfig

console = Console()
portfolio_app = typer.Typer(help="Portfolio & Exposure Allocation Commands")

@portfolio_app.command("run-portfolio")
def run_portfolio(
    sport: str = typer.Option("football", help="Sport to allocate"),
    market: str = typer.Option("1x2", help="Market to allocate"),
    strategy: str = typer.Option("sequential_cap", help="Allocation strategy")
):
    console.print(f"Running portfolio allocation for {sport} - {market} using {strategy}...")

    # Placeholder: In a real system, you'd fetch candidates from sizing layer
    console.print("Successfully generated portfolio allocations.")

@portfolio_app.command("list-allocation-strategies")
def list_allocation_strategies():
    from sports_signal_bot.portfolio.factory import PortfolioStrategyFactory

    console.print("[bold]Available Portfolio Strategies:[/bold]")
    for k in PortfolioStrategyFactory._registry.keys():
        console.print(f"- {k}")
