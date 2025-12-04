#!/usr/bin/env python3
"""
Integrate generated infographic images into Beginner DeFi Concepts gitbook markdown files.
Reads asset specifications and inserts image references at appropriate locations.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GitBookImageIntegrator:
    """Integrates images into gitbook markdown files"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize integrator with paths"""
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.specs_path = self.base_dir.parent.parent / 'assets' / 'infographics' / 'scripts' / 'beginner_defi_concepts_asset_specs.json'
        self.images_source = self.base_dir.parent.parent / 'assets' / 'infographics' / 'output' / 'beginner-defi-concepts'
        self.images_dest = self.base_dir / 'content' / 'images'
        self.lessons_dir = self.base_dir / 'content' / 'lessons'
        self.exercises_dir = self.base_dir / 'content' / 'exercises'
        
        # Load asset specifications
        with open(self.specs_path, 'r') as f:
            self.specs = json.load(f)
    
    def find_insertion_point(self, content: str, placement: str, asset_title: str) -> Optional[int]:
        """
        Find insertion point in markdown content based on placement description.
        
        Args:
            content: Full markdown content
            placement: Placement description from specs (e.g., "After 'The AMM Revolution' section")
            asset_title: Asset title for context
        
        Returns:
            Index where image should be inserted, or None if not found
        """
        # Extract section name from placement
        # Patterns: "After 'Section Name' section", "After 'Section Name'", etc.
        match = re.search(r"['\"]([^'\"]+)['\"]", placement)
        if not match:
            return None
        
        section_name = match.group(1)
        
        # Try to find the section header
        # Look for headers containing the section name
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Check if line is a header and contains the section name
            if line.startswith('#') and section_name.lower() in line.lower():
                # Find the end of this section (next header of same or higher level)
                header_level = len(line) - len(line.lstrip('#'))
                
                # Look for next section
                for j in range(i + 1, len(lines)):
                    next_line = lines[j]
                    if next_line.strip() and next_line.startswith('#'):
                        next_level = len(next_line) - len(next_line.lstrip('#'))
                        if next_level <= header_level:
                            # Found next section, insert before it
                            return '\n'.join(lines[:j]).__len__() if j > 0 else None
                
                # If no next section found, insert after a few paragraphs
                # Find a good spot (after 2-3 paragraphs or at end of section)
                insert_idx = i + 1
                paragraph_count = 0
                for j in range(i + 1, min(i + 20, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        if not lines[j].strip().startswith('-') and not lines[j].strip().startswith('*'):
                            paragraph_count += 1
                            if paragraph_count >= 2:
                                insert_idx = j + 1
                                break
                
                # Calculate position
                return '\n'.join(lines[:insert_idx]).__len__() + (1 if insert_idx < len(lines) else 0)
        
        # Fallback: search for section name in content (case-insensitive)
        pattern = re.compile(re.escape(section_name), re.IGNORECASE)
        matches = list(pattern.finditer(content))
        if matches:
            # Use first match and insert after it
            match_pos = matches[0].end()
            # Find next newline or paragraph break
            next_newline = content.find('\n\n', match_pos)
            if next_newline != -1:
                return next_newline + 2
            return match_pos
        
        return None
    
    def get_image_path(self, asset_id: str, lesson_id: Optional[str] = None, exercise_id: Optional[str] = None) -> str:
        """Get relative image path for markdown"""
        if lesson_id:
            # Format: images/lessons/lesson_01/bdc01_01_money_evolution_timeline.png
            lesson_num = lesson_id.replace('lesson_', '')
            return f"images/lessons/lesson_{lesson_num:0>2}/{asset_id}_*.png"
        elif exercise_id:
            exercise_num = exercise_id.replace('exercise_', '')
            return f"images/exercises/exercise_{exercise_num:0>2}/{asset_id}_*.png"
        return ""
    
    def get_actual_image_filename(self, asset_id: str, lesson_id: Optional[str] = None, exercise_id: Optional[str] = None) -> Optional[Path]:
        """Get actual image filename from destination directory"""
        if lesson_id:
            lesson_num = lesson_id.replace('lesson_', '')
            dest_dir = self.images_dest / 'lessons' / f"lesson_{lesson_num:0>2}"
        elif exercise_id:
            exercise_num = exercise_id.replace('exercise_', '')
            dest_dir = self.images_dest / 'exercises' / f"exercise_{exercise_num:0>2}"
        else:
            return None
        
        # Find file matching asset_id
        pattern = f"{asset_id}_*.png"
        matches = list(dest_dir.glob(pattern))
        if matches:
            return matches[0]
        return None
    
    def insert_image_reference(self, content: str, insertion_point: int, image_path: str, asset_title: str) -> str:
        """Insert image markdown reference at specified point"""
        # Create image markdown
        image_markdown = f"\n\n![{asset_title}]({image_path})\n\n"
        
        # Insert at position
        return content[:insertion_point] + image_markdown + content[insertion_point:]
    
    def integrate_lesson(self, lesson_id: str, dry_run: bool = False) -> Dict:
        """Integrate images for a specific lesson"""
        lesson_num = int(lesson_id.replace('lesson_', ''))
        lesson_file = self.lessons_dir / f"lesson-{lesson_num:02d}-*.md"
        
        # Find actual lesson file
        matches = list(self.lessons_dir.glob(f"lesson-{lesson_num:02d}-*.md"))
        if not matches:
            return {'error': f"Lesson file not found for {lesson_id}"}
        
        lesson_file = matches[0]
        
        # Get lesson assets
        lesson_data = self.specs.get('lessons', {}).get(lesson_id)
        if not lesson_data:
            return {'error': f"No assets found for {lesson_id}"}
        
        # Read lesson content
        with open(lesson_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = []
        
        # Process each asset
        for asset in lesson_data['assets']:
            asset_id = asset['asset_id']
            asset_title = asset['title']
            placement = asset.get('placement', '')
            
            # Check if image already exists in content with correct path
            # Look for image markdown with this asset_id or title
            image_pattern = re.compile(rf'!\[.*?\]\(.*?{re.escape(asset_id)}.*?\)', re.IGNORECASE)
            if image_pattern.search(content):
                results.append({
                    'asset_id': asset_id,
                    'status': 'skipped',
                    'reason': 'Already exists in content with correct path'
                })
                continue
            
            # Check for old cloud URLs and replace them
            old_url_pattern = re.compile(rf'!\[.*?{re.escape(asset_title)}.*?\]\(https?://[^\)]+\)', re.IGNORECASE)
            old_match = old_url_pattern.search(content)
            if old_match:
                # Replace old URL with new local path
                image_file = self.get_actual_image_filename(asset_id, lesson_id=lesson_id)
                if image_file and image_file.exists():
                    lesson_num = int(lesson_id.replace('lesson_', ''))
                    image_rel_path = f"images/lessons/lesson_{lesson_num:02d}/{image_file.name}"
                    content = old_url_pattern.sub(f'![{asset_title}]({image_rel_path})', content)
                    results.append({
                        'asset_id': asset_id,
                        'status': 'replaced',
                        'old_url': old_match.group(0),
                        'new_path': image_rel_path
                    })
                    continue
            
            # Find insertion point
            insertion_point = self.find_insertion_point(content, placement, asset_title)
            
            if insertion_point is None:
                # Try alternative: find by section keywords
                # Extract keywords from placement
                keywords = re.findall(r'\b\w+\b', placement.lower())
                insertion_point = None
                for keyword in keywords:
                    if len(keyword) > 4:  # Skip short words
                        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                        matches = list(pattern.finditer(content))
                        if matches:
                            # Insert after first match
                            match_pos = matches[0].end()
                            next_para = content.find('\n\n', match_pos)
                            insertion_point = next_para + 2 if next_para != -1 else match_pos
                            break
            
            if insertion_point is None:
                results.append({
                    'asset_id': asset_id,
                    'status': 'failed',
                    'reason': f'Could not find insertion point for: {placement}'
                })
                continue
            
            # Get image path
            image_file = self.get_actual_image_filename(asset_id, lesson_id=lesson_id)
            if not image_file or not image_file.exists():
                results.append({
                    'asset_id': asset_id,
                    'status': 'failed',
                    'reason': f'Image file not found: {image_file}'
                })
                continue
            
            # Get relative path for markdown
            image_rel_path = f"images/lessons/lesson_{lesson_num:02d}/{image_file.name}"
            
            # Insert image
            if not dry_run:
                content = self.insert_image_reference(content, insertion_point, image_rel_path, asset_title)
                results.append({
                    'asset_id': asset_id,
                    'status': 'inserted',
                    'insertion_point': insertion_point,
                    'image_path': image_rel_path
                })
            else:
                results.append({
                    'asset_id': asset_id,
                    'status': 'would_insert',
                    'insertion_point': insertion_point,
                    'image_path': image_rel_path
                })
        
        # Write updated content
        if not dry_run and results:
            with open(lesson_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            'lesson_id': lesson_id,
            'lesson_file': str(lesson_file),
            'results': results
        }
    
    def integrate_exercise(self, exercise_id: str, dry_run: bool = False) -> Dict:
        """Integrate images for a specific exercise"""
        exercise_num = int(exercise_id.replace('exercise_', ''))
        
        # Find actual exercise file
        matches = list(self.exercises_dir.glob(f"exercise-{exercise_num:02d}-*.md"))
        if not matches:
            return {'error': f"Exercise file not found for {exercise_id}"}
        
        exercise_file = matches[0]
        
        # Get exercise assets
        exercise_data = self.specs.get('exercises', {}).get(exercise_id)
        if not exercise_data:
            return {'error': f"No assets found for {exercise_id}"}
        
        # Read exercise content
        with open(exercise_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = []
        
        # Process each asset
        for asset in exercise_data['assets']:
            asset_id = asset['asset_id']
            asset_title = asset['title']
            placement = asset.get('placement', '')
            
            # Check if image already exists in content with correct path
            image_pattern = re.compile(rf'!\[.*?\]\(.*?{re.escape(asset_id)}.*?\)', re.IGNORECASE)
            if image_pattern.search(content):
                results.append({
                    'asset_id': asset_id,
                    'status': 'skipped',
                    'reason': 'Already exists in content with correct path'
                })
                continue
            
            # Check for old cloud URLs and replace them
            old_url_pattern = re.compile(rf'!\[.*?{re.escape(asset_title)}.*?\]\(https?://[^\)]+\)', re.IGNORECASE)
            old_match = old_url_pattern.search(content)
            if old_match:
                # Replace old URL with new local path
                image_file = self.get_actual_image_filename(asset_id, exercise_id=exercise_id)
                if image_file and image_file.exists():
                    exercise_num = int(exercise_id.replace('exercise_', ''))
                    image_rel_path = f"images/exercises/exercise_{exercise_num:02d}/{image_file.name}"
                    content = old_url_pattern.sub(f'![{asset_title}]({image_rel_path})', content)
                    results.append({
                        'asset_id': asset_id,
                        'status': 'replaced',
                        'old_url': old_match.group(0),
                        'new_path': image_rel_path
                    })
                    continue
            
            # Find insertion point
            insertion_point = self.find_insertion_point(content, placement, asset_title)
            
            if insertion_point is None:
                # Try alternative search
                keywords = re.findall(r'\b\w+\b', placement.lower())
                insertion_point = None
                for keyword in keywords:
                    if len(keyword) > 4:
                        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                        matches = list(pattern.finditer(content))
                        if matches:
                            match_pos = matches[0].end()
                            next_para = content.find('\n\n', match_pos)
                            insertion_point = next_para + 2 if next_para != -1 else match_pos
                            break
            
            if insertion_point is None:
                results.append({
                    'asset_id': asset_id,
                    'status': 'failed',
                    'reason': f'Could not find insertion point for: {placement}'
                })
                continue
            
            # Get image path
            image_file = self.get_actual_image_filename(asset_id, exercise_id=exercise_id)
            if not image_file or not image_file.exists():
                results.append({
                    'asset_id': asset_id,
                    'status': 'failed',
                    'reason': f'Image file not found: {image_file}'
                })
                continue
            
            # Get relative path
            image_rel_path = f"images/exercises/exercise_{exercise_num:02d}/{image_file.name}"
            
            # Insert image
            if not dry_run:
                content = self.insert_image_reference(content, insertion_point, image_rel_path, asset_title)
                results.append({
                    'asset_id': asset_id,
                    'status': 'inserted',
                    'insertion_point': insertion_point,
                    'image_path': image_rel_path
                })
            else:
                results.append({
                    'asset_id': asset_id,
                    'status': 'would_insert',
                    'insertion_point': insertion_point,
                    'image_path': image_rel_path
                })
        
        # Write updated content
        if not dry_run and results:
            with open(exercise_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            'exercise_id': exercise_id,
            'exercise_file': str(exercise_file),
            'results': results
        }
    
    def integrate_all(self, dry_run: bool = False) -> Dict:
        """Integrate images for all lessons and exercises"""
        results = {
            'lessons': [],
            'exercises': []
        }
        
        # Process lessons
        for lesson_id in sorted(self.specs.get('lessons', {}).keys()):
            result = self.integrate_lesson(lesson_id, dry_run=dry_run)
            results['lessons'].append(result)
        
        # Process exercises
        for exercise_id in sorted(self.specs.get('exercises', {}).keys()):
            result = self.integrate_exercise(exercise_id, dry_run=dry_run)
            results['exercises'].append(result)
        
        return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Integrate images into Beginner DeFi Concepts gitbook markdown files')
    parser.add_argument('--lesson', help='Integrate specific lesson (e.g., lesson_01)')
    parser.add_argument('--exercise', help='Integrate specific exercise (e.g., exercise_01)')
    parser.add_argument('--all', action='store_true', help='Integrate all lessons and exercises')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    integrator = GitBookImageIntegrator()
    
    if args.all:
        results = integrator.integrate_all(dry_run=args.dry_run)
        print(f"\n{'DRY RUN: ' if args.dry_run else ''}Integration complete!")
        print(f"Lessons processed: {len(results['lessons'])}")
        print(f"Exercises processed: {len(results['exercises'])}")
    elif args.lesson:
        result = integrator.integrate_lesson(args.lesson, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
    elif args.exercise:
        result = integrator.integrate_exercise(args.exercise, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
    else:
        print("Usage:")
        print("  Integrate all: python integrate_gitbook_images.py --all")
        print("  Integrate lesson: python integrate_gitbook_images.py --lesson lesson_01")
        print("  Integrate exercise: python integrate_gitbook_images.py --exercise exercise_01")
        print("  Dry run: python integrate_gitbook_images.py --all --dry-run")

