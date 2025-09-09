"""
Display utilities for showing execution results
"""

import logging
from .utils import Colors


def display_execution_summary(results, output_dir):
    """Display the final execution summary"""
    if not results:
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}📊 EXECUTION SUMMARY 📊{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    
    success_rate = (results['successful']/results['total']*100)
    success_color = Colors.GREEN if success_rate >= 80 else Colors.YELLOW if success_rate >= 50 else Colors.RED
    
    print(f"{Colors.BOLD}📈 Total test cases:{Colors.END} {Colors.WHITE}{results['total']}{Colors.END}")
    print(f"{Colors.BOLD}✅ Successful:{Colors.END} {Colors.GREEN}{results['successful']}{Colors.END}")
    print(f"{Colors.BOLD}❌ Failed:{Colors.END} {Colors.RED}{results['failed']}{Colors.END}")
    print(f"{Colors.BOLD}📊 Success rate:{Colors.END} {success_color}{success_rate:.1f}%{Colors.END}")
    
    # Show execution time statistics if available
    if 'total_execution_time' in results:
        print(f"{Colors.BOLD}⏱️  Total execution time:{Colors.END} {Colors.WHITE}{results['total_execution_time']:.2f}s{Colors.END}")
        print(f"{Colors.BOLD}📊 Average execution time:{Colors.END} {Colors.WHITE}{results['average_execution_time']:.2f}s{Colors.END}")
        print(f"{Colors.BOLD}⚡ Fastest test case:{Colors.END} {Colors.GREEN}{results['min_execution_time']:.2f}s{Colors.END}")
        print(f"{Colors.BOLD}🐌 Slowest test case:{Colors.END} {Colors.RED}{results['max_execution_time']:.2f}s{Colors.END}")
    
    print(f"\n{Colors.BOLD}📁 Results saved in:{Colors.END} {Colors.BLUE}{output_dir}/{Colors.END}")
    print(f"{Colors.BOLD}📝 Log file:{Colors.END} {Colors.BLUE}test_execution.log{Colors.END}")
    
    # Show detailed results
    if results['details']:
        print(f"\n{Colors.BOLD}📋 Detailed Results:{Colors.END}")
        for detail in results['details']:
            status_icon = "✅" if detail['success'] else "❌"
            status_color = Colors.GREEN if detail['success'] else Colors.RED
            execution_time = f" ({detail['execution_time']:.2f}s)" if detail['execution_time'] else ""
            print(f"  {status_icon} {Colors.WHITE}ID {detail['id']}{Colors.END} - {Colors.CYAN}{detail['codename']}{Colors.END} - {status_color}{'PASS' if detail['success'] else 'FAIL'}{Colors.END}{execution_time}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")


def log_execution_info(args):
    """Log execution configuration information"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting AIP Test Executor")
    logger.info(f"Test cases file: {args.test_cases}")
    logger.info(f"Output directory: {args.output}")
    if args.specific_ids:
        logger.info(f"Running specific IDs: {args.specific_ids}")
    else:
        logger.info("Running all test cases")
    
    if args.sequential:
        logger.info("Running in SEQUENTIAL mode")
    else:
        logger.info(f"Running in PARALLEL mode with {args.workers} workers")
    
    logger.info("AIP agents will run with --verbose flag for detailed output")
