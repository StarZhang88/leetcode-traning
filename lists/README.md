# Problem List Format

## File Naming

Problem list files should be placed in the `lists/` directory with the format: `<name>.json`

Examples:
- `leetcode_60.json` - 60 LeetCode problems
- `leetcode_top100.json` - Top 100 problems
- `company_google.json` - Google company problems

## JSON Structure

```json
{
  "version": 1,                    // Required: version number for future compatibility
  "default_plan": {                // Required: default study plan
    "new_per_day": 2,              // Required: number of new problems per day
    "review_per_day": 3,           // Required: number of review problems per day
    "review_days": [2, 7, 21]      // Required: review interval days array
  },
  "problems": [                     // Required: problem list
    {
      "id": 1,                     // Required: problem ID
      "title": "Two Sum",          // Required: problem title
      "difficulty": "easy",        // Optional: difficulty (easy/medium/hard)
      "tags": ["hash", "array"],   // Optional: tags array
      "star": true                 // Optional: whether marked (priority practice)
    }
  ]
}
```

## Field Descriptions

### Top-level Fields

- `version` (required): Integer, current version is 1
- `default_plan` (required): Object containing default study plan configuration
- `problems` (required): Array of problems

### default_plan Fields

- `new_per_day` (required): Integer, number of new problems per day
- `review_per_day` (required): Integer, number of review problems per day
- `review_days` (required): Integer array, review interval days, e.g., `[2, 7, 21]` means review on days 2, 7, and 21

### Problem Object in problems Array

- `id` (required): Integer, LeetCode problem ID
- `title` (required): String, problem title
- `difficulty` (optional): String, difficulty level, usually "easy", "medium", or "hard"
- `tags` (optional): String array, problem tags
- `star` (optional): Boolean, whether marked as important problem (priority practice)

## Usage Examples

```bash
# Use default list (leetcode_60)
python tools/practice.py

# Use specified list
python tools/practice.py --list leetcode_top100

# List all available lists
python tools/practice.py --list-catalog

# Customize new and review counts
python tools/practice.py --list leetcode_60 --new 3 --review 5
```

## Structure Analysis

The current structure design is reasonable:

✅ **Advantages:**
1. Version number supports future extensions
2. Default plan configuration is flexible and can be overridden via command line
3. Problem fields are complete, supporting difficulty, tags, and priority marking
4. Optional fields are well-designed, not forcing all fields to be required

💡 **Optional Improvements:**
1. Can add `description` field for list description
2. Can add `created_at` / `updated_at` fields for version management
3. Can add `name` field in `default_plan` for list name

The current structure is sufficient for use and does not require mandatory modifications.
