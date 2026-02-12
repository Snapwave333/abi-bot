from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import time
import os

from utils import setup_logging, get_env, generate_event_id
from scraper import ESSScraper
from gcal import GoogleCalendarManager

# Initialize logging
logger = setup_logging()
console = Console()

def run_bot():
    console.clear()
    console.print(Panel.fit("[bold orange1]ABI Bot Sync v3.0[/bold orange1]", subtitle="Automated Schedule Sync (Optimized)"))

    # Load Config
    try:
        venue_id = get_env("ESS_VENUE_ID", required=True)
        username = get_env("ESS_USERNAME", required=True)
        password = get_env("ESS_PASSWORD", required=True)
        headless = get_env("HEADLESS", "False").lower() == "true"
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        logger.error(str(e))
        return

    # Step 1: Google API
    gcal = None
    with console.status("[bold green]Initializing Google Calendar API...[/bold green]", spinner="dots"):
        try:
            gcal = GoogleCalendarManager()
            console.print("[bold green]✓ Google Service Initialized[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to init Google Service: {e}[/bold red]")
            return

    # Step 2: Scrape ESS
    console.print("\n[bold cyan]Step 2: Scrape ESS Schedule[/bold cyan]")
    
    scraper = ESSScraper(venue_id, username, password, headless=headless)
    events = []
    
    with console.status("[bold blue]Running Scraper...[/bold blue]", spinner="earth"):
        events = scraper.scrape_schedule()

    if not events:
        console.print("[yellow]No events found or scraping failed (check logs).[/yellow]")
        return

    console.print(f"[bold green]✓ Found {len(events)} events.[/bold green]")

    # Step 3: Sync
    console.print("\n[bold cyan]Step 3: Syncing to Google Calendar[/bold cyan]")
    
    table = Table(title="Sync Results", show_header=True, header_style="bold magenta")
    table.add_column("Date", style="cyan")
    table.add_column("Event", style="white")
    table.add_column("Time", style="yellow")
    table.add_column("Status", style="green")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Syncing events...", total=len(events))
        
        for evt in events:
            uid = generate_event_id(evt['summary'], evt['start'], evt['end'])
            status = gcal.sync_event(evt, uid)
            
            status_display = status
            if status == "ADDED":
                status_display = "[green]ADDED[/green]"
            elif status == "SKIPPED":
                status_display = "[dim]SKIPPED[/dim]"
            else:
                status_display = f"[bold red]{status}[/bold red]"

            table.add_row(
                evt['start'].strftime('%Y-%m-%d'),
                evt['summary'],
                evt['time_str'],
                status_display
            )
            progress.advance(task)

    console.print(table)
    console.print(Panel("[bold green]Sync Process Completed Successfully![/bold green]"))
    time.sleep(5)

if __name__ == "__main__":
    run_bot()
