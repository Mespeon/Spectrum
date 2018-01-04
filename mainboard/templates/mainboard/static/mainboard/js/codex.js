/*
Codex Script Sheet
for Spectrum Business Management System v.1.0
Created by Mark Nolledo for exclusive use
Do not use or access without permission.
*/

function validateForm() {

}

function deleteStorePrompt() {
		prompt = confirm("Are you sure you want to DELETE this store?")
		if (prompt == true) {
			return true;
		}
		else {
			return false;
		}
}

function cancelPrompt() {
	prompt = confirm("Are you sure you want to DELETE this advice?\nThis action is equivalent to completely deleting this advice from the database.");
	if (prompt == true) {
		return true;
	}
	else {
		return false;
	}
}

function approvePrompt() {
	prompt = confirm("Are you sure you want to APPROVE this advice?\nThis action is equivalent to finalizing the advice. Once approved, the advice is no longer editable nor removable from the database.");
	if (prompt == true) {
		return true;
	}
	else {
		return false;
	}
}
